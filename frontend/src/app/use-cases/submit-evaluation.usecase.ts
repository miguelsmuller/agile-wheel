import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { AgileWheelBackEndHTTP } from '@client/agile-wheel-backend.http';
import {
  Activity,
  DimensionWithScores,
  Participant,
} from '@models/activity.model';
import { clearDataFromLocalStorage } from '@utils/utils';

export interface SubmitEvaluationResponse {
  participant: Participant;
  activity: Activity;
}

export interface SubmitEvaluationRatingRequest {
  principle_id: string;
  score: number;
  comments: string;
}

export interface SubmitEvaluationRequest {
  ratings: SubmitEvaluationRatingRequest[];
}

@Injectable({ providedIn: 'root' })
export class SubmitEvaluationService {
  constructor(
    private backendClient: AgileWheelBackEndHTTP,
    private router: Router
  ) {}

  submitEvaluation(
    activityId: string,
    participantId: string,
    dimensions: DimensionWithScores[]
  ): void {
    const apiEndPoint = `v1/activity/${activityId}/evaluation`;
    const payload = this.buildSubmitEvaluationPayload(dimensions);
    const headers = { 'X-Participant-Id': participantId };

    this.backendClient
      .post<SubmitEvaluationResponse>(apiEndPoint, payload, headers)
      .subscribe({
        next: () => {
          const redirectTo = `activity/${activityId}/result`;
          clearDataFromLocalStorage();
          this.router.navigate([redirectTo]);
        },
        error: error => {
          console.error('Erro ao criar atividade:', error);
        },
      });
  }

  private buildSubmitEvaluationPayload(
    dimensions: DimensionWithScores[]
  ): SubmitEvaluationRequest {
    const ratings = dimensions.flatMap(dimension =>
      dimension.principles.map(principle => ({
        principle_id: principle.id as string,
        score: principle.score || 0,
        comments: principle.comments || '',
      }))
    );

    return { ratings };
  }
}
