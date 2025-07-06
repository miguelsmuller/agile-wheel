import { InjectionToken } from '@angular/core';

import { Activity, Participant } from 'domain/model';

/**
 * Application port for closing an activity use-case.
 */
export const CLOSE_ACTIVITY_USE_CASE_PORT = new InjectionToken<CloseActivityUseCasePort>(
  'CloseActivityUseCasePort'
);

export interface CloseActivityUseCasePort {
  execute(activity: Activity, currentParticipant: Participant): void;
}
