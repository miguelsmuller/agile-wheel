import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Observable } from 'rxjs';

const WS_HOST = 'ws://localhost:3333';

@Injectable({
  providedIn: 'root'
})
export class AgileWheelBackEndWS {
  private socket$: WebSocketSubject<any> | null = null;

  private currentEndpoint: string | null = null;

  connect(path: string): Observable<any> {
    const fullEndpoint = `${WS_HOST}${path}`;

    if (!this.socket$ || this.socket$.closed || this.currentEndpoint !== fullEndpoint) {
      this.socket$ = webSocket(fullEndpoint);
      this.currentEndpoint = fullEndpoint;
    }

    return this.socket$.asObservable();
  }

  disconnect(): void {
    this.socket$?.complete();
    this.socket$ = null;
    this.currentEndpoint = null;
  }
}
