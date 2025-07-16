import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';

import { AgileWheelBackEndHTTP } from 'adapters/http/agile-wheel-backend.http';
import { GetActivityResultResponse } from 'application/dtos/get-activity-result.dto';
import { GetActivityResultUseCasePort } from 'application/ports/get-activity-result-use-case-port';

@Injectable({ providedIn: 'root' })
export class GetActivityResultUseCase implements GetActivityResultUseCasePort {
  constructor(private readonly backendClient: AgileWheelBackEndHTTP) {}

  execute(activityId: string): Observable<GetActivityResultResponse> {
    const apiEndPoint = `v1/activity/${activityId}/result`;
    return this.backendClient.get<GetActivityResultResponse>(apiEndPoint);
  }
}
