import { InjectionToken } from '@angular/core';
import { Activity, Participant, DimensionWithScores } from 'domain/model';

/**
 * Application port for the activity flow use-case.
 */
export const ACTIVITY_FLOW_USE_CASE_PORT = new InjectionToken<ActivityFlowUseCasePort>(
  'ActivityFlowUseCasePort'
);

export interface ActivityFlowUseCasePort {
  execute(
    activity: Activity,
    participant: Participant,
    evaluation: DimensionWithScores[]
  ): Promise<void>;
}
