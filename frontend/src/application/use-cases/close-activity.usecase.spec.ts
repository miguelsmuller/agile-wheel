import { TestBed } from '@angular/core/testing';

import { of } from 'rxjs';

import { AgileWheelBackEndHTTP } from 'adapters/http/agile-wheel-backend.http';
import { activityFixture, regularParticipantFixture } from '@test/fixtures';

import { CloseActivityUserCase } from './close-activity.usecase';

describe('CloseActivityUserCase', () => {
  let usecase: CloseActivityUserCase;

  let httpSpy: jasmine.SpyObj<AgileWheelBackEndHTTP>;

  beforeEach(() => {
    httpSpy = jasmine.createSpyObj<AgileWheelBackEndHTTP>('AgileWheelBackEndHTTP', ['post']);
    httpSpy.post.and.returnValue(of({}));

    TestBed.configureTestingModule({
      providers: [CloseActivityUserCase, { provide: AgileWheelBackEndHTTP, useValue: httpSpy }],
    });

    usecase = TestBed.inject(CloseActivityUserCase);
  });

  it('should call backend with correct endpoint and headers', () => {
    // WHEN
    usecase.execute(activityFixture, regularParticipantFixture);

    // THEN
    expect(httpSpy.post).toHaveBeenCalledWith(
      `v1/activity/${activityFixture.activity_id}/close`,
      '',
      {
        'X-Participant-Id': regularParticipantFixture.id,
      }
    );
  });
});
