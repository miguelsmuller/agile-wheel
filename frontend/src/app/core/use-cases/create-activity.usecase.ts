import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

import { AgileWheelBackEndClient } from '../../client/agile-wheel-backend.client';
import { Activity, Participant } from '../../core/models/activity.model';

export interface CreateActivityResponse {
  owner: Participant;
  activity: Activity;
}

export interface CreateActivityRequest {
  owner_name: string;
  owner_email: string;
}

@Injectable({ providedIn: 'root' })
export class CreateActivityService {
  constructor(
    private backendClient: AgileWheelBackEndClient,
    private router: Router
  ) {}

  createActivity(owner: CreateActivityRequest): void {
    this.backendClient.post<CreateActivityResponse>('v1/activity', owner).subscribe({
      next: (response) => {
        localStorage.setItem('participant', JSON.stringify(response.owner));
        localStorage.setItem('activity', JSON.stringify(response.activity));

        this.router.navigate(['/activity', response.activity.activity_id]);
      },
      error: (error) => {
        console.error('Erro ao criar atividade:', error);
      }
    });
  }
}
