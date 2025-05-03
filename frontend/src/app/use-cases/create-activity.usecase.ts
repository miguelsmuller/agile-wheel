import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { AgileWheelBackEndHTTP } from '@client/agile-wheel-backend.http';
import { Activity, Participant } from '@models/activity.model';
import { setActivityToLocalStorage, setParticipantToLocalStorage } from '@utils/utils';


export interface CreateActivityResponse {
  participant: Participant;
  activity: Activity;
}

export interface CreateActivityRequest {
  name: string;
  email: string;
}

@Injectable({ providedIn: 'root' })
export class CreateActivityService {
  constructor(
    private backendClient: AgileWheelBackEndHTTP,
    private router: Router
  ) {}

  createActivity(owner: CreateActivityRequest): void {
    this.backendClient.post<CreateActivityResponse>('v1/activity', {
      owner: owner
    }).subscribe({
      next: (response) => {

        setParticipantToLocalStorage(response.participant)
        setActivityToLocalStorage(response.activity)

        this.router.navigate(['/activity', response.activity.activity_id]);
      },
      error: (error) => {
        console.error('Erro ao criar atividade:', error);
      }
    });
  }
}
