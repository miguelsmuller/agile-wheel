import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { Observable, timer } from 'rxjs';
import { retry } from 'rxjs/operators';

import { environment } from '@env/environment';

@Injectable({
  providedIn: 'root',
})
export class AgileWheelBackEndWS {
  private socket$: WebSocketSubject<unknown> | null = null;
  private currentEndpoint: string | null = null;
  private readonly APIBaseURL = environment.wsAgileWheelUrl;
  public wsFactory = webSocket;

  connect<T>(path: string): Observable<T> {
    const fullEndpoint = `${this.APIBaseURL}${path}`;

    if (!this.socket$ || this.socket$.closed || this.currentEndpoint !== fullEndpoint) {
      this.currentEndpoint = fullEndpoint;
      this.socket$ = this.wsFactory({
        url: fullEndpoint,
        openObserver: {
          next: () => {
            // istanbul ignore next
            console.log('[AW-WS] Connected'); // NOSONAR
          },
        },
        closeObserver: {
          next: () => {
            // istanbul ignore next
            console.log('[AW-WS] Disconnected'); // NOSONAR
          },
        },
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

  disconnect(): void {
    this.socket$?.complete();
    this.socket$ = null;
    this.currentEndpoint = null;
  }

  sendMessage<T>(message: T): void {
    if (this.isConnected()) {
      (this.socket$ as WebSocketSubject<T>)?.next(message);
    }
  }

  isConnected(): boolean {
    return !!this.socket$ && !this.socket$.closed;
  }
}
