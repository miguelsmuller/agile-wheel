import { InjectionToken } from '@angular/core';

import { Observable } from 'rxjs';

import { EnterActivityRequest, EnterActivityResponse } from 'application/dtos/enter-activity.dto';

/**
 * Application port for entering an existing activity use-case.
 */
export const ENTER_ACTIVITY_USE_CASE_PORT = new InjectionToken<EnterActivityUseCasePort>(
  'EnterActivityUseCasePort'
);

export interface EnterActivityUseCasePort {
  execute(
    activityId: string,
    participant: EnterActivityRequest
  ): Observable<EnterActivityResponse>;
}
