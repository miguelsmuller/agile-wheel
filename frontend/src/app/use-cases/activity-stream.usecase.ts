import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { AgileWheelBackEndWS } from '../client/agile-wheel-backend.ws';

export interface ActivityStreamMessage {
  activity_id: string;
  created_at: string;
  is_opened: boolean;
  participants: Participant[];
}

export interface Participant {
  id: string;
  name: string;
  email: string;
}

@Injectable({ providedIn: 'root' })
export class ActivityStreamUseCase {
  constructor(private socketClient: AgileWheelBackEndWS) {}

  startObserving(
    activityID: string,
    participantID: string
  ): Observable<ActivityStreamMessage> {
    const path = `/v1/activities/${activityID}/stream?participant_id=${participantID}`;

    return this.socketClient
      .connect<ActivityStreamMessage>(path)
      .pipe(map((msg: ActivityStreamMessage) => msg));
  }

  stopObserving() {
    this.socketClient.disconnect();
  }
}
