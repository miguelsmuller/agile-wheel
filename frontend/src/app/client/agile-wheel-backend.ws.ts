import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Observable, timer } from 'rxjs';
import { retry } from 'rxjs/operators';

const WS_HOST = 'ws://localhost:3333';

@Injectable({
  providedIn: 'root',
})
export class AgileWheelBackEndWS {
  private socket$: WebSocketSubject<unknown> | null = null;
  private currentEndpoint: string | null = null;

  connect<T>(path: string): Observable<T> {
    const fullEndpoint = `${WS_HOST}${path}`;

    if (!this.socket$ || this.socket$.closed || this.currentEndpoint !== fullEndpoint) {
      this.currentEndpoint = fullEndpoint;
      this.socket$ = webSocket({
        url: fullEndpoint,
        openObserver: { next: () => console.log('[WS] Connected') },
        closeObserver: { next: () => console.log('[WS] Disconnected') },
      });
    }

    const typedSocket$ = this.socket$ as WebSocketSubject<T>;

    return typedSocket$.pipe(
      retry({
        count: Infinity,
        delay: (error, retryCount) => {
          console.warn(`[WS] Error, attempt #${retryCount}, retrying in 3s...`, error);
          return timer(3000);
        },
      })
    );
  }

  sendMessage<T>(message: T): void {
    if (this.isConnected()) {
      (this.socket$ as WebSocketSubject<T>)?.next(message);
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
