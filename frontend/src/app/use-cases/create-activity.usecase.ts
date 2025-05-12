import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { AgileWheelBackEndHTTP } from '@client/agile-wheel-backend.http';
import { Activity, Participant } from '@models/activity.model';
import { setActivityToLocalStorage, setParticipantToLocalStorage } from '@utils/utils';
import { Observable, tap } from 'rxjs';

export interface CreateActivityResponse {
  participant: Participant;
  activity: Activity;
}

export interface CreateActivityRequest {
  name: string;
  email: string;
}

@Injectable({ providedIn: 'root' })
export class CreateActivityService {
  constructor(
    private readonly backendClient: AgileWheelBackEndHTTP,
    private readonly router: Router
  ) {}

  createActivity(participant: CreateActivityRequest): Observable<CreateActivityResponse> {
    const apiEndPoint = 'v1/activity';
    const payload = {
      owner: participant,
    };

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
