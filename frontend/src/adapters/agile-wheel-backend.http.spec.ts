import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

import { AgileWheelBackEndHTTP } from './agile-wheel-backend.http';
import { environment } from '@env/environment';

describe('AgileWheelBackEndHTTP', () => {
  let service: AgileWheelBackEndHTTP;
  let httpMock: HttpTestingController;
  const dummy = { foo: 'bar' };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting(), AgileWheelBackEndHTTP],
    });

    service = TestBed.inject(AgileWheelBackEndHTTP);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('should perform GET with correct URL & headers', () => {
    // WHEN
    service
      .get('xpto', { Authorization: 'Bearer tok' })
      .subscribe(res => expect(res).toEqual(dummy));

    // THEN
    const req = httpMock.expectOne(`${environment.apiAgileWheelUrl}/xpto`);
    expect(req.request.method).toBe('GET');
    expect(req.request.headers.get('Authorization')).toBe('Bearer tok');

    req.flush(dummy);
  });

  it('should perform POST with correct URL & body', () => {
    // WHEN
    service.post('xpto', { x: 1 }).subscribe(res => expect(res).toEqual(dummy));

    // THEN
    const req = httpMock.expectOne(`${environment.apiAgileWheelUrl}/xpto`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ x: 1 });

    req.flush(dummy);
  });
});
