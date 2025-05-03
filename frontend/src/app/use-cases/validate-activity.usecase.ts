import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, firstValueFrom } from 'rxjs';

import { AgileWheelBackEndClient } from '../client/agile-wheel-backend.client';
import { Activity, Participant } from '../models/activity.model';
import { parseJSON } from '../utils/utils';

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
    private backendClient: AgileWheelBackEndClient,
    private router: Router
  ) {}

  async initialize(activityId: string): Promise<{ activity: Activity, currentParticipant: Participant }> {
    if (!activityId) this.redirectToCreateActivity('Missing activity ID');

    const activity = this.getActivityFromLocalStorage();
    const participant = this.getParticipantFromLocalStorage();

    if (!activity || !participant) {
      this.redirectToCreateActivity('Missing data in localStorage');
    }

    if (activityId !== activity.activity_id) {
      this.redirectToCreateActivity('Activity ID mismatch');
    }

    const backendActivity = await this.fetchActivityFromBackend(activityId, participant.id);

    if (!backendActivity || backendActivity.activity_id !== activity.activity_id) {
      this.redirectToCreateActivity('Activity not valid from backend');
    }

    localStorage.setItem('activity', JSON.stringify(backendActivity));

    this.activitySubject.next(backendActivity);
    this.participantSubject.next(participant);

    return { activity: backendActivity, currentParticipant: participant };
  }

  private getActivityFromLocalStorage(): Activity | null {
    const raw = localStorage.getItem('activity');
    return raw ? parseJSON<Activity>(raw) : null;
  }

  private getParticipantFromLocalStorage(): Participant | null {
    const raw = localStorage.getItem('participant');
    return raw ? parseJSON<Participant>(raw) : null;
  }

  private async fetchActivityFromBackend(activityId: string, participantId: string): Promise<Activity | null> {
    try {
      const response = await firstValueFrom(
        this.backendClient.get<GetActivityResponse>(
          `v1/activity/${activityId}`,
          { 'X-Participant-Id': participantId }
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