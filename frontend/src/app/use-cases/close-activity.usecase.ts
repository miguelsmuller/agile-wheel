import { Injectable } from '@angular/core';

import { AgileWheelBackEndHTTP } from '@client/agile-wheel-backend.http';
import { Activity, Participant } from '@models/activity.model';

export interface CloseActivityResponse {
  activity: Activity;
}

/**
 * Service responsible for closing an activity in the backend.
 */
@Injectable({ providedIn: 'root' })
export class CloseActivityService {
  constructor(private readonly backendClient: AgileWheelBackEndHTTP) {}

  /**
   * Closes an activity in the backend.
   *
   * @param activity - The activity to be closed.
   * @param currentParticipant - The participant requesting to close the activity.
   */
  closeActivity(activity: Activity, currentParticipant: Participant): void {
    const apiEndPoint = `v1/activity/${activity.activity_id}/close`;
    const payload = '';
    const headers = { 'X-Participant-Id': currentParticipant.id };

    this.backendClient.post<CloseActivityResponse>(apiEndPoint, payload, headers).subscribe({
      next: (response: CloseActivityResponse) => {
        console.debug('[CloseActivityService] Starting close activity', response);
      },
      error: error => {
        console.error('[CloseActivityService] Error while close activity', error);
      },
    });
  }
}
