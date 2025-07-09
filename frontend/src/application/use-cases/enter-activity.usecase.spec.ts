import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import { of } from 'rxjs';

import { AgileWheelBackEndHTTP } from 'adapters/http/agile-wheel-backend.http';
import { clearDataFromLocalStorage } from 'adapters/local-storage/utils';
import { EnterActivityRequest, EnterActivityResponse } from 'application/dtos/enter-activity.dto';
import { activityFixture, regularParticipantFixture } from 'testing/fixtures';

import { EnterActivityUseCase } from './enter-activity.usecase';

describe('EnterActivityUseCase', () => {
  let usecase: EnterActivityUseCase;

  let httpSpy: jasmine.SpyObj<AgileWheelBackEndHTTP>;
  let routerSpy: jasmine.SpyObj<Router>;

  const request: EnterActivityRequest = { name: 'John', email: 'j@x' };
  const response: EnterActivityResponse = {
    participant: regularParticipantFixture,
    activity: activityFixture,
  };

  beforeEach(() => {
    httpSpy = jasmine.createSpyObj<AgileWheelBackEndHTTP>('AgileWheelBackEndHTTP', ['patch']);
    routerSpy = jasmine.createSpyObj<Router>('Router', ['navigate']);

    clearDataFromLocalStorage();

    TestBed.configureTestingModule({
      providers: [
        EnterActivityUseCase,
        { provide: AgileWheelBackEndHTTP, useValue: httpSpy },
        { provide: Router, useValue: routerSpy },
      ],
    });

    usecase = TestBed.inject(EnterActivityUseCase);
  });

  it('should patch join request and store response', done => {
    // GIVEN
    httpSpy.patch.and.returnValue(of(response));

    // WHEN
    usecase.execute('a1', request).subscribe(res => {
      // THEN
      expect(res).toEqual(response);
      expect(localStorage.getItem('participant')).toEqual(
        JSON.stringify(regularParticipantFixture)
      );
      expect(localStorage.getItem('activity')).toEqual(JSON.stringify(activityFixture));
      expect(routerSpy.navigate).toHaveBeenCalledWith(['/activity/', activityFixture.activity_id]);
      done();
    });

    expect(httpSpy.patch).toHaveBeenCalledWith('v1/activity/a1/join', { participant: request });
  });
});
