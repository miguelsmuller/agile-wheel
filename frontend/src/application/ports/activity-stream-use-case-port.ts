import { InjectionToken } from '@angular/core';
import { Observable } from 'rxjs';
import { ActivityStreamMessage } from 'application/dtos/activity-stream.dto';

/**
 * Application port for observing activity stream use-case.
 */
export const ACTIVITY_STREAM_USE_CASE_PORT = new InjectionToken<ActivityStreamUseCasePort>(
  'ActivityStreamUseCasePort'
);

export interface ActivityStreamUseCasePort {
  startObserving(activityID: string, participantID: string): Observable<ActivityStreamMessage>;

  stopObserving(): void;
}
