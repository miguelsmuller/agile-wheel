import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';

import { AgileWheelBackEndHTTP } from '@adapters/agile-wheel-backend.http';
import { Activity } from '@models/activity.model';
import { getActivityFromLocalStorage, getParticipantFromLocalStorage } from '@utils/utils';

export interface GetActivityResponse {
  activity: Activity;
}

@Injectable({ providedIn: 'root' })
export class ValidateActitivityGuard implements CanActivate {
  constructor(
    private readonly router: Router,
    private readonly awClient: AgileWheelBackEndHTTP
  ) {}

  async canActivate(route: ActivatedRouteSnapshot): Promise<boolean> {
    const activityIdFromURL = route.paramMap.get('id');

    if (!activityIdFromURL) {
      this.redirectToCreateActivity('Missing activity ID');
      return false;
    }

    const activityFromLocalStorage = getActivityFromLocalStorage();
    const currentParticipant = getParticipantFromLocalStorage();

    const hasLocalStorageData = !activityFromLocalStorage || !currentParticipant;
    if (hasLocalStorageData) {
      this.redirectToCreateActivity('Missing localStorage data');
      return false;
    }

    const isActivityIdMismatched = activityIdFromURL !== activityFromLocalStorage.activity_id;
    if (isActivityIdMismatched) {
      this.redirectToCreateActivity('Activity mismatch');
      return false;
    }

    const remoteActivity = await this.fetchActivityFromBackend(
      activityIdFromURL,
      currentParticipant.id
    );

    const isLocalActivityInvalid =
      !remoteActivity || remoteActivity.activity_id !== activityFromLocalStorage.activity_id;
    if (isLocalActivityInvalid) {
      this.redirectToCreateActivity('Activity invalid');
      return false;
    }

    return true;
  }

  private async fetchActivityFromBackend(
    activityId: string,
    participantId: string
  ): Promise<Activity | null> {
    try {
      const response = await firstValueFrom(
        this.awClient.get<GetActivityResponse>(`v1/activity/${activityId}`, {
          'X-Participant-Id': participantId,
        })
      );
      return response.activity;
    } catch (error) {
      console.error('[ActivityStateGuard] Error fetching activity: ', error);
      return null;
    }
  }

  private redirectToCreateActivity(message: string): void {
    console.error('[ActivityStateGuard] Something went wrong.', message);
    this.router.navigate(['/create-activity']);
  }
}
