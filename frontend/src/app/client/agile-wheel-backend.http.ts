import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AgileWheelBackEndHTTP {
  private readonly baseUrl = 'http://localhost:3333';

  constructor(private http: HttpClient) {}

  private createHeaders(
    headers?: Record<string, string>
  ): HttpHeaders | undefined {
    return headers ? new HttpHeaders(headers) : undefined;
  }

  get<T>(endpoint: string, headers?: Record<string, string>): Observable<T> {
    return this.http.get<T>(`${this.baseUrl}/${endpoint}`, {
      headers: this.createHeaders(headers),
    });
  }

  post<T>(
    endpoint: string,
    body: unknown,
    headers?: Record<string, string>
  ): Observable<T> {
    return this.http.post<T>(`${this.baseUrl}/${endpoint}`, body, {
      headers: this.createHeaders(headers),
    });
  }

  put<T>(
    endpoint: string,
    body: unknown,
    headers?: Record<string, string>
  ): Observable<T> {
    return this.http.put<T>(`${this.baseUrl}/${endpoint}`, body, {
      headers: this.createHeaders(headers),
    });
  }

  delete<T>(endpoint: string, headers?: Record<string, string>): Observable<T> {
    return this.http.delete<T>(`${this.baseUrl}/${endpoint}`, {
      headers: this.createHeaders(headers),
    });
  }
}
