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

  it('should perform PUT with correct URL & body & headers', () => {
    // WHEN
    service
      .put('xpto', { x: 2 }, { 'X-Header': 'H-Value' })
      .subscribe(res => expect(res).toEqual(dummy));

    // THEN
    const req = httpMock.expectOne(`${environment.apiAgileWheelUrl}/xpto`);
    expect(req.request.method).toBe('PUT');
    expect(req.request.body).toEqual({ x: 2 });
    expect(req.request.headers.get('X-Header')).toBe('H-Value');

    req.flush(dummy);
  });

  it('should perform PATCH with correct URL & body & headers', () => {
    // WHEN
    service
      .patch('xpto', { y: 3 }, { 'Y-Header': 'Y-Value' })
      .subscribe(res => expect(res).toEqual(dummy));

    // THEN
    const req = httpMock.expectOne(`${environment.apiAgileWheelUrl}/xpto`);
    expect(req.request.method).toBe('PATCH');
    expect(req.request.body).toEqual({ y: 3 });
    expect(req.request.headers.get('Y-Header')).toBe('Y-Value');

    req.flush(dummy);
  });

  it('should perform DELETE with correct URL & headers', () => {
    // WHEN
    service.delete('xpto', { 'D-Header': 'D-Value' }).subscribe(res => expect(res).toEqual(dummy));

    // THEN
    const req = httpMock.expectOne(`${environment.apiAgileWheelUrl}/xpto`);
    expect(req.request.method).toBe('DELETE');
    expect(req.request.headers.get('D-Header')).toBe('D-Value');

    req.flush(dummy);
  });
});
