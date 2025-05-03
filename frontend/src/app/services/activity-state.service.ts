import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, firstValueFrom } from 'rxjs';

import { AgileWheelBackEndHTTP } from '@client/agile-wheel-backend.http';
import { Activity, Participant } from '@models/activity.model';
import { parseJSON } from '@utils/utils';

export interface GetActivityResponse {
  activity: Activity;
}

@Injectable({ providedIn: 'root' })
export class ActivityStateService {
  private activitySubject = new BehaviorSubject<Activity | null>(null);
  private participantSubject = new BehaviorSubject<Participant | null>(null);

  activity$ = this.activitySubject.asObservable();
  participant$ = this.participantSubject.asObservable();

  constructor(
    private awClient: AgileWheelBackEndHTTP,
    private router: Router
  ) {}

  async initialize(activityId: string): Promise<{ activity: Activity, currentParticipant: Participant }> {
    if (!activityId) this.redirectToCreateActivity('Missing activity ID');

    const Localactivity = this.getActivityFromLocalStorage();
    const currentParticipant = this.getParticipantFromLocalStorage();

    const hasLocalStorageData = (!Localactivity || !currentParticipant)
    if (hasLocalStorageData) {
      this.redirectToCreateActivity('Missing localStorage data'); 
    }

    const isActivityIdMismatched = (activityId !== Localactivity.activity_id)
    if (isActivityIdMismatched) {
      this.redirectToCreateActivity('Activity mismatch');
    }

    const remoteActivity = await this.fetchActivityFromBackend(
      activityId, currentParticipant.id
    );

    const isLocalActivityInvalid = (
      !remoteActivity || remoteActivity.activity_id !== Localactivity.activity_id
    )
    if (isLocalActivityInvalid) {
      this.redirectToCreateActivity('Activity invalid');
    }

    localStorage.setItem('activity', JSON.stringify(remoteActivity));

    this.activitySubject.next(remoteActivity);
    this.participantSubject.next(currentParticipant);

    return { 
      activity: remoteActivity, 
      currentParticipant: currentParticipant 
    };
  }

  private getActivityFromLocalStorage(): Activity | null {
    const raw = localStorage.getItem('activity');
    return (raw) ? parseJSON<Activity>(raw) : null;
  }

  private getParticipantFromLocalStorage(): Participant | null {
    const raw = localStorage.getItem('participant');
    return (raw) ? parseJSON<Participant>(raw) : null;
  }

  private async fetchActivityFromBackend(
    activityId: string, participantId: string
  ): Promise<Activity | null> {
    try {
      const response = await firstValueFrom(
        this.awClient.get<GetActivityResponse>(
          `v1/activity/${activityId}`,
          { 'X-Participant-Id': participantId }
        )
      );
      return response.activity;

    } catch (error) {
      console.error('[ActivityStateService] Error fetching activity: ', error);
      return null;
    }
  }

  private redirectToCreateActivity(message: string): never {
    this.router.navigate(['/create-activity']);
    throw new Error(message);
  }
}