import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { AgileWheelBackEndHTTP } from '@client/agile-wheel-backend.http';
import { Activity, DimensionWithScores, Participant } from '@models/activity.model';


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
    const payload = this.buildSubmitEvaluationPayload(dimensions);
    
    this.backendClient.post<SubmitEvaluationResponse>(
      `v1/activity/${activityId}/evaluation`, 
      payload, 
      { "X-Participant-Id": participantId }
    ).subscribe({
      next: (response) => {
        console.log(response)
        this.router.navigate(['/result']);
      },
      error: (error) => {
        console.error('Erro ao criar atividade:', error);
      }
    });
  }

  private buildSubmitEvaluationPayload(
    dimensions: DimensionWithScores[]
  ): SubmitEvaluationRequest {
    const ratings = dimensions.flatMap(dimension =>
      dimension.principles.map(principle => ({
        principle_id: principle.id as string,
        score: principle.score || 0,
        comments: principle.comments || ''
      }))
    );

    return { ratings };
  }
}
