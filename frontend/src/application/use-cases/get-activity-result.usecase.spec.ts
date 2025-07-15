import { TestBed } from '@angular/core/testing';

import { of } from 'rxjs';

import { AgileWheelBackEndHTTP } from 'adapters/http/agile-wheel-backend.http';
import { GetActivityResultResponse } from 'application/dtos/get-activity-result.dto';

import { GetActivityResultUseCase } from './get-activity-result.usecase';

describe('GetActivityResultUseCase', () => {
  let usecase: GetActivityResultUseCase;
  let httpSpy: jasmine.SpyObj<AgileWheelBackEndHTTP>;

  beforeEach(() => {
    httpSpy = jasmine.createSpyObj<AgileWheelBackEndHTTP>('AgileWheelBackEndHTTP', ['get']);

    TestBed.configureTestingModule({
      providers: [GetActivityResultUseCase, { provide: AgileWheelBackEndHTTP, useValue: httpSpy }],
    });

    usecase = TestBed.inject(GetActivityResultUseCase);
  });

  it('should call backend with correct endpoint', done => {
    const response: GetActivityResultResponse = {
      activity: { activity_id: 'a1', created_at: 'now', is_opened: false },
      result: { overall_score: 0, dimension_scores: [] },
    };
    httpSpy.get.and.returnValue(of(response));

    usecase.execute('a1').subscribe(res => {
      expect(res).toEqual(response);
      done();
    });

    expect(httpSpy.get).toHaveBeenCalledWith('v1/activity/a1/result');
  });
});
