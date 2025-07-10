import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import { of } from 'rxjs';

import { AgileWheelBackEndHTTP } from 'adapters/http/agile-wheel-backend.http';
import { clearDataFromLocalStorage } from 'adapters/local-storage/utils';
import {
  CreateActivityRequest,
  CreateActivityResponse,
} from 'application/dtos/create-activity.dto';
import { activityFixture, ownerParticipantFixture } from '@test/fixtures';

import { CreateActivityUseCase } from './create-activity.usecase';

describe('CreateActivityUseCase', () => {
  let usecase: CreateActivityUseCase;

  let httpSpy: jasmine.SpyObj<AgileWheelBackEndHTTP>;
  let routerSpy: jasmine.SpyObj<Router>;

  const request: CreateActivityRequest = { name: 'John', email: 'j@x' };
  const response: CreateActivityResponse = {
    participant: ownerParticipantFixture,
    activity: activityFixture,
  };

  beforeEach(() => {
    httpSpy = jasmine.createSpyObj<AgileWheelBackEndHTTP>('AgileWheelBackEndHTTP', ['post']);
    routerSpy = jasmine.createSpyObj<Router>('Router', ['navigate']);

    clearDataFromLocalStorage();

    TestBed.configureTestingModule({
      providers: [
        CreateActivityUseCase,
        { provide: AgileWheelBackEndHTTP, useValue: httpSpy },
        { provide: Router, useValue: routerSpy },
      ],
    });

    usecase = TestBed.inject(CreateActivityUseCase);
  });

  it('should post create request and store response', done => {
    // GIVEN
    httpSpy.post.and.returnValue(of(response));

    // WHEN
    usecase.execute(request).subscribe(res => {
      // THEN
      expect(res).toEqual(response);
      expect(localStorage.getItem('participant')).toEqual(JSON.stringify(ownerParticipantFixture));
      expect(localStorage.getItem('activity')).toEqual(JSON.stringify(activityFixture));
      expect(routerSpy.navigate).toHaveBeenCalledWith(['/activity/', activityFixture.activity_id]);
      done();
    });

    expect(httpSpy.post).toHaveBeenCalledWith('v1/activity', { owner: request });
  });
});
