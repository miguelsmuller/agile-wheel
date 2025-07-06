import { TestBed } from '@angular/core/testing';

import { Subject } from 'rxjs';
import type { WebSocketSubject } from 'rxjs/webSocket';

import { AgileWheelBackEndWS } from './agile-wheel-backend.ws';

describe('AgileWheelBackEndWS', () => {
  let service: AgileWheelBackEndWS;
  let mockSocket$: WebSocketSubject<unknown>;

  beforeEach(() => {
    mockSocket$ = new Subject() as WebSocketSubject<unknown>;

    TestBed.configureTestingModule({ providers: [AgileWheelBackEndWS] });

    service = TestBed.inject(AgileWheelBackEndWS);

    spyOn(service, 'wsFactory').and.returnValue(mockSocket$);
  });

  it('should connect and return an observable', () => {
    // WHEN
    const obs = service.connect<unknown>('/path');
    obs.subscribe();

    // THEN
    expect(service.wsFactory).toHaveBeenCalled();
  });

  it('isConnected should reflect socket state', () => {
    // WHEN
    service.connect<unknown>('/path');

    // THEN
    expect(service.isConnected()).toBeTrue();

    // GIVEN
    service.disconnect();

    // THEN
    expect(service.isConnected()).toBeFalse();
  });

  it('should send messages when connected', () => {
    // GIVEN
    const nextSpy = spyOn(mockSocket$, 'next');
    service.connect<unknown>('/path');

    // WHEN
    service.sendMessage({ foo: 'bar' });

    // THEN
    expect(nextSpy).toHaveBeenCalledWith({ foo: 'bar' });
  });
});
