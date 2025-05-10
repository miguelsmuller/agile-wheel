import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { AgileWheelBackEndHTTP } from '@client/agile-wheel-backend.http';
import { Activity, Participant } from '@models/activity.model';
import { setActivityToLocalStorage, setParticipantToLocalStorage } from '@utils/utils';

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

  enterActivity(activityId: string, participant: EnterActivityRequest): void {
    const apiEndPoint = `v1/activity/${activityId}/join`;
    const payload = {
      participant: participant,
    };

    this.backendClient.patch<EnterActivityResponse>(apiEndPoint, payload).subscribe({
      next: response => {
        setParticipantToLocalStorage(response.participant);
        setActivityToLocalStorage(response.activity);

        this.router.navigate(['/activity', response.activity.activity_id]);
      },
      error: error => {
        console.error('Erro ao criar atividade:', error);
      },
    });
  }
}
