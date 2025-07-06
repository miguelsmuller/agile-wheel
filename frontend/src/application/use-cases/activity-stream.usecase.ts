import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { AgileWheelBackEndWS } from 'adapters/agile-wheel-backend.ws';
import { ActivityStreamMessage } from 'application/dtos/activity-stream.dto';
import { ActivityStreamUseCasePort } from 'application/ports/activity-stream-use-case-port';

interface BackendEnvelope {
  type: string;
  activity_id: string;
  activity: ActivityStreamMessage;
}

@Injectable({ providedIn: 'root' })
export class ActivityStreamUseCase implements ActivityStreamUseCasePort {
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
