import { Injectable } from '@angular/core';

import { AgileWheelBackEndHTTP } from 'adapters/agile-wheel-backend.http';
import { Activity, DimensionWithScores, Participant } from 'domain/model';
import {
  SubmitEvaluationRequest,
  SubmitEvaluationResponse,
} from 'application/dtos/submit-evaluation.dto';
import { SubmitEvaluationUseCasePort } from 'application/ports/submit-evaluation-use-case-port';

/**
 * Service responsible for submitting participant evaluations to the backend.
 */
@Injectable({ providedIn: 'root' })
export class SubmitEvaluationUseCase implements SubmitEvaluationUseCasePort {
  constructor(private readonly backendClient: AgileWheelBackEndHTTP) {}

  /**
   * Submits a participant's evaluation for a specific activity.
   *
   * @param activity - The activity being evaluated.
   * @param currentParticipant - The participant submitting the evaluation.
   * @param dimensions - The dimensions and principles being evaluated with scores.
   */
  execute(
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
