import { InjectionToken } from '@angular/core';
import { Observable } from 'rxjs';
import {
  CreateActivityRequest,
  CreateActivityResponse,
} from 'application/dtos/create-activity.dto';

/**
 * Application port for creating a new activity use-case.
 */
export const CREATE_ACTIVITY_USE_CASE_PORT = new InjectionToken<CreateActivityUseCasePort>(
  'CreateActivityUseCasePort'
);

export interface CreateActivityUseCasePort {
  execute(request: CreateActivityRequest): Observable<CreateActivityResponse>;
}
