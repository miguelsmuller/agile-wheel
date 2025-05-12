import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { AgileWheelBackEndHTTP } from '@client/agile-wheel-backend.http';
import { Activity, DimensionWithScores, Participant } from '@models/activity.model';
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
    private readonly backendClient: AgileWheelBackEndHTTP,
    private readonly router: Router
  ) {}

  submitEvaluation(
    activity: Activity,
    currentParticipant: Participant,
    dimensions: DimensionWithScores[]
  ): void {
    const apiEndPoint = `v1/activity/${activity.activity_id}/evaluation`;
    const payload = this.buildSubmitEvaluationPayload(dimensions);
    const headers = { 'X-Participant-Id': currentParticipant.id };

    this.backendClient.post<SubmitEvaluationResponse>(apiEndPoint, payload, headers).subscribe({
      next: (response: SubmitEvaluationResponse) => {
        console.debug('[SubmitEvaluationService] Starting subimit evaluation', response);

        const redirectTo = `activity/${activity.activity_id}/result`;
        clearDataFromLocalStorage();
        this.router.navigate([redirectTo]);
      },
      error: error => {
        console.error('[SubmitEvaluationService] Error while submit evaluation', error);
      },
    });
  }

  private buildSubmitEvaluationPayload(
    dimensions: DimensionWithScores[]
  ): SubmitEvaluationRequest {
    const ratings = dimensions.flatMap(dimension =>
      dimension.principles.map(principle => ({
        principle_id: principle.id,
        score: principle.score || 0,
        comments: principle.comments || '',
      }))
    );

    return { ratings };
  }
}
