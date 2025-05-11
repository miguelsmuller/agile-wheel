import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, Router } from '@angular/router';
import { AgileWheelBackEndHTTP } from '@client/agile-wheel-backend.http';
import { Activity } from '@models/activity.model';
import { getActivityFromLocalStorage, getParticipantFromLocalStorage } from '@utils/utils';
import { firstValueFrom } from 'rxjs';

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

    const LocalActivity = getActivityFromLocalStorage();
    const currentParticipant = getParticipantFromLocalStorage();

    const hasLocalStorageData = !LocalActivity || !currentParticipant;
    if (hasLocalStorageData) {
      this.redirectToCreateActivity('Missing localStorage data');
      return false;
    }

    const isActivityIdMismatched = activityIdFromURL !== LocalActivity.activity_id;
    if (isActivityIdMismatched) {
      this.redirectToCreateActivity('Activity mismatch');
      return false;
    }

    const remoteActivity = await this.fetchActivityFromBackend(
      activityIdFromURL,
      currentParticipant.id
    );

    const isLocalActivityInvalid =
      !remoteActivity || remoteActivity.activity_id !== LocalActivity.activity_id;
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

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  private redirectToCreateActivity(message: string): void {
    this.router.navigate(['/create-activity']);
  }
}
