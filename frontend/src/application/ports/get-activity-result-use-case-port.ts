import { InjectionToken } from '@angular/core';

import { Observable } from 'rxjs';

import { GetActivityResultResponse } from 'application/dtos/get-activity-result.dto';

/**
 * Application port for get result use-case.
 */
export const GET_ACTIVITY_RESULT_USE_CASE_PORT = new InjectionToken<GetActivityResultUseCasePort>(
  'GetActivityResultUseCasePort'
);

export interface GetActivityResultUseCasePort {
  execute(activityId: string): Observable<GetActivityResultResponse>;
}
