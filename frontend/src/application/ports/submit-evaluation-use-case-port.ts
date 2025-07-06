import { InjectionToken } from '@angular/core';
import { Activity, Participant, DimensionWithScores } from 'domain/model';

/**
 * Application port for submitting an evaluation use-case.
 */
export const SUBMIT_EVALUATION_USE_CASE_PORT = new InjectionToken<SubmitEvaluationUseCasePort>(
  'SubmitEvaluationUseCasePort'
);

export interface SubmitEvaluationUseCasePort {
  execute(
    activity: Activity,
    currentParticipant: Participant,
    dimensions: DimensionWithScores[]
  ): void;
}
