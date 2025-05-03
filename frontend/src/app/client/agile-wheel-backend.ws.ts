import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Observable, timer } from 'rxjs';
import { retry } from 'rxjs/operators';

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
      this.currentEndpoint = fullEndpoint;
      this.socket$ = webSocket({
        url: fullEndpoint,
        openObserver: { next: () => console.log('[WS] Connected') },
        closeObserver: { next: () => console.log('[WS] Disconnected') },
      });
    }

    return this.socket$.pipe(
      retry({
        count: Infinity,
        delay: (error, retryCount) => {
          console.warn(`[WS] Error, attempt #${retryCount}, retrying in 3s...`, error);
          return timer(3000);
        }
      })
    );
  }

  sendMessage(message: any): void {
    if (this.isConnected()) {
      this.socket$?.next(message);
    }
  }

  isConnected(): boolean {
    return !!this.socket$ && !this.socket$.closed;
  }

  disconnect(): void {
    this.socket$?.complete();
    this.socket$ = null;
    this.currentEndpoint = null;
  }
}
