import { Injectable } from '@angular/core';
import { Observable, Subscription } from 'rxjs';
import { map } from 'rxjs/operators';

import { AgileWheelBackEndWS } from '../client/agile-wheel-backend.ws';

export interface ActivityStreamMessage {
  value: number;
}

@Injectable({ providedIn: 'root' })
export class ActivityStreamUseCase {
  constructor(private socketClient: AgileWheelBackEndWS) {}

  observeStatus(): Observable<ActivityStreamMessage> {
    return this.socketClient.connect("/v1/activity-stream").pipe(
      map((msg: ActivityStreamMessage) => ({
        value: msg.value * 10
      }))
    );
  }

  stopObserving() {
    this.socketClient.disconnect();
  }
}
