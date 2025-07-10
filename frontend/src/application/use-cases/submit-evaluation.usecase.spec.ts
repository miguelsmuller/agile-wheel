import { TestBed } from '@angular/core/testing';

import { of } from 'rxjs';

import { AgileWheelBackEndHTTP } from 'adapters/http/agile-wheel-backend.http';
import { activityFixture, ownerParticipantFixture, dimensionsFixture } from '@test/fixtures';

import { SubmitEvaluationUseCase } from './submit-evaluation.usecase';

describe('SubmitEvaluationUseCase', () => {
  let usecase: SubmitEvaluationUseCase;
  let httpSpy: jasmine.SpyObj<AgileWheelBackEndHTTP>;

  beforeEach(() => {
    httpSpy = jasmine.createSpyObj<AgileWheelBackEndHTTP>('AgileWheelBackEndHTTP', ['post']);
    httpSpy.post.and.returnValue(of({}));

    TestBed.configureTestingModule({
      providers: [SubmitEvaluationUseCase, { provide: AgileWheelBackEndHTTP, useValue: httpSpy }],
    });

    usecase = TestBed.inject(SubmitEvaluationUseCase);
  });

  it('should post evaluation with built payload', () => {
    // WHEN
    usecase.execute(activityFixture, ownerParticipantFixture, dimensionsFixture);

    // THEN
    expect(httpSpy.post).toHaveBeenCalledWith(
      `v1/activity/${activityFixture.activity_id}/evaluation`,
      { ratings: [{ principle_id: 'p', score: 2, comments: '' }] },
      { 'X-Participant-Id': ownerParticipantFixture.id }
    );
  });
});
