import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { AgileWheelBackEndWS } from '@adapters/agile-wheel-backend.ws';

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

interface BackendEnvelope {
  type: string;
  activity_id: string;
  activity: ActivityStreamMessage;
}

@Injectable({ providedIn: 'root' })
export class ActivityStreamUseCase {
  constructor(private readonly socketClient: AgileWheelBackEndWS) {}

  startObserving(activityID: string, participantID: string): Observable<ActivityStreamMessage> {
    const path = `/v1/activities/${activityID}/stream?participant_id=${participantID}`;

    return this.socketClient
      .connect<BackendEnvelope>(path)
      .pipe(map((msg: BackendEnvelope) => msg.activity));
  }

  stopObserving() {
    this.socketClient.disconnect();
  }
}
