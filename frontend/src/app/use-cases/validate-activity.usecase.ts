import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { firstValueFrom } from 'rxjs';

import { AgileWheelBackEndClient } from '../client/agile-wheel-backend.client';
import { Activity, Participant } from '../models/activity.model';
import { parseJSON } from '../utils/utils';

export interface GetActivityResponse {
  activity: Activity;
}

@Injectable({ providedIn: 'root' })
export class ValidateActivityService {
  constructor(
    private backendClient: AgileWheelBackEndClient,
    private router: Router
  ) {}

  async validate(activityId: string): Promise<Activity> {
    if (!activityId) {
      this.redirectToCreateActivity('No activity ID found given');
    }
    
    const activityStringFromLocalStorage = localStorage.getItem('activity');
    const participantStringFromLocalStorage = localStorage.getItem('participant');

    if (!activityStringFromLocalStorage || !participantStringFromLocalStorage) {
      this.redirectToCreateActivity('No data found in localStorage');
    }

    const activityFromLocalStorage = parseJSON<Activity>(activityStringFromLocalStorage);
    const participantFromLocalStorage = parseJSON<Participant>(participantStringFromLocalStorage);

    if (activityId !== activityFromLocalStorage.activity_id) {
      this.redirectToCreateActivity('Activity ID from URL does not match');
    }

    const activityFromBackEnd = await this.getActivityFromBackEnd(
      activityId, participantFromLocalStorage.id
    );

    if (!activityFromBackEnd) {
      this.redirectToCreateActivity('Activity not found in backend');
    }

    if (activityFromBackEnd.activity_id !== activityFromLocalStorage.activity_id) {
      this.redirectToCreateActivity('Activity ID from backend does not match');
    }

    return activityFromLocalStorage
  }

  private async getActivityFromBackEnd(
    activityID: string, participantID: string
  ): Promise<Activity | null> {
    try {
      const response = await firstValueFrom(
        this.backendClient.get<GetActivityResponse>(
          `v1/activity/${activityID}`,
          { 'X-Participant-Id': participantID }
        )
      );
      return response.activity;
    } catch (error) {
      console.error('Erro ao consultar atividade:', error);
      return null;
    }
  }

  private redirectToCreateActivity(message: string): never {
    this.router.navigate(['/create-activity']);
    throw new Error(message);
  }
}
