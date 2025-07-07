import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { Observable, tap } from 'rxjs';

import { AgileWheelBackEndHTTP } from 'adapters/http/agile-wheel-backend.http';
import {
  setActivityToLocalStorage,
  setParticipantToLocalStorage,
} from 'adapters/local-storage/utils';
import {
  CreateActivityRequest,
  CreateActivityResponse,
} from 'application/dtos/create-activity.dto';
import { CreateActivityUseCasePort } from 'application/ports/create-activity-use-case-port';

@Injectable({ providedIn: 'root' })
export class CreateActivityUseCase implements CreateActivityUseCasePort {
  constructor(
    private readonly backendClient: AgileWheelBackEndHTTP,
    private readonly router: Router
  ) {}

  execute(request: CreateActivityRequest): Observable<CreateActivityResponse> {
    const apiEndPoint = 'v1/activity';
    const payload = { owner: request };

    return this.backendClient.post<CreateActivityResponse>(apiEndPoint, payload).pipe(
      tap((response: CreateActivityResponse) => {
        setParticipantToLocalStorage(response.participant);
        setActivityToLocalStorage(response.activity);
        console.debug('[CreateActivityService] Activity created successfully', response);

        this.router.navigate(['/activity/', response.activity.activity_id]);
      })
    );
  }
}
