import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { AgileWheelBackEndHTTP } from '@adapters/agile-wheel-backend.http';
import { Activity, Participant } from '@models/activity.model';
import { setActivityToLocalStorage, setParticipantToLocalStorage } from '@utils/utils';
import { tap } from 'rxjs';

export interface EnterActivityResponse {
  participant: Participant;
  activity: Activity;
}

export interface EnterActivityRequest {
  name: string;
  email: string;
}

@Injectable({ providedIn: 'root' })
export class EnterActivityService {
  constructor(
    private readonly backendClient: AgileWheelBackEndHTTP,
    private readonly router: Router
  ) {}

  enterActivity(activityId: string, participant: EnterActivityRequest) {
    const apiEndPoint = `v1/activity/${activityId}/join`;
    const payload = {
      participant: participant,
    };

    return this.backendClient.patch<EnterActivityResponse>(apiEndPoint, payload).pipe(
      tap((response: EnterActivityResponse) => {
        setParticipantToLocalStorage(response.participant);
        setActivityToLocalStorage(response.activity);
        console.debug('[EnterActivityService] Enter activity successfully', response);

        this.router.navigate(['/activity/', response.activity.activity_id]);
      })
    );
  }
}
