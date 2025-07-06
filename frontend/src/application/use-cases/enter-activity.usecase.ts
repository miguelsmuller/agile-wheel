import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { tap } from 'rxjs';

import { AgileWheelBackEndHTTP } from 'adapters/http/agile-wheel-backend.http';
import {
  setActivityToLocalStorage,
  setParticipantToLocalStorage,
} from 'adapters/local-storage/utils';
import { EnterActivityRequest, EnterActivityResponse } from 'application/dtos/enter-activity.dto';
import { EnterActivityUseCasePort } from 'application/ports/enter-activity-use-case-port';

@Injectable({ providedIn: 'root' })
export class EnterActivityUseCase implements EnterActivityUseCasePort {
  constructor(
    private readonly backendClient: AgileWheelBackEndHTTP,
    private readonly router: Router
  ) {}

  execute(activityId: string, participant: EnterActivityRequest) {
    const apiEndPoint = `v1/activity/${activityId}/join`;
    const payload = {
      participant: participant,
    };

    return this.backendClient.patch<EnterActivityResponse>(apiEndPoint, payload).pipe(
      tap((response: EnterActivityResponse) => {
        setParticipantToLocalStorage(response.participant);
        setActivityToLocalStorage(response.activity);
        console.debug('[EnterActivityService] Enter activity successfully', response);

        this.router.navigate(['/activity/', response.activity.activity_id]);
      })
    );
  }
}
