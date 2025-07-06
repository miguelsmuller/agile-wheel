import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';

import { environment } from 'environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AgileWheelBackEndHTTP {
  private readonly baseUrl = environment.apiAgileWheelUrl;

  constructor(private readonly http: HttpClient) {}

  private createHeaders(headers?: Record<string, string>): HttpHeaders | undefined {
    return headers ? new HttpHeaders(headers) : undefined;
  }

  get<T>(endpoint: string, headers?: Record<string, string>): Observable<T> {
    console.debug('[AW-GET]', `${this.baseUrl}/${endpoint}`);
    return this.http.get<T>(`${this.baseUrl}/${endpoint}`, {
      headers: this.createHeaders(headers),
    });
  }

  post<T>(endpoint: string, body: unknown, headers?: Record<string, string>): Observable<T> {
    console.debug('[AW-POST]', `${this.baseUrl}/${endpoint}`);
    return this.http.post<T>(`${this.baseUrl}/${endpoint}`, body, {
      headers: this.createHeaders(headers),
    });
  }

  put<T>(endpoint: string, body: unknown, headers?: Record<string, string>): Observable<T> {
    console.debug('[AW-PUT]', `${this.baseUrl}/${endpoint}`);
    return this.http.put<T>(`${this.baseUrl}/${endpoint}`, body, {
      headers: this.createHeaders(headers),
    });
  }

  patch<T>(endpoint: string, body: unknown, headers?: Record<string, string>): Observable<T> {
    console.debug('[AW-PATCH]', `${this.baseUrl}/${endpoint}`);
    return this.http.patch<T>(`${this.baseUrl}/${endpoint}`, body, {
      headers: this.createHeaders(headers),
    });
  }

  delete<T>(endpoint: string, headers?: Record<string, string>): Observable<T> {
    console.debug('[AW-DELETE]', `${this.baseUrl}/${endpoint}`);
    return this.http.delete<T>(`${this.baseUrl}/${endpoint}`, {
      headers: this.createHeaders(headers),
    });
  }
}
