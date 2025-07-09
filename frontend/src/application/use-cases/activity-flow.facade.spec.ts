import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import {
  activityFixture,
  regularParticipantFixture,
  ownerParticipantFixture,
} from 'testing/fixtures';

import { ActivityFlowFacade } from './activity-flow.facade';
import { CloseActivityUserCase } from './close-activity.usecase';
import { SubmitEvaluationUseCase } from './submit-evaluation.usecase';

describe('ActivityFlowFacade', () => {
  let facade: ActivityFlowFacade;

  let submitSpy: jasmine.SpyObj<SubmitEvaluationUseCase>;
  let closeSpy: jasmine.SpyObj<CloseActivityUserCase>;

  let routerSpy: jasmine.SpyObj<Router>;

  beforeEach(() => {
    submitSpy = jasmine.createSpyObj<SubmitEvaluationUseCase>('SubmitEvaluationUseCase', [
      'execute',
    ]);
    closeSpy = jasmine.createSpyObj<CloseActivityUserCase>('CloseActivityUserCase', ['execute']);
    routerSpy = jasmine.createSpyObj<Router>('Router', ['navigate']);

    localStorage.setItem('activity', JSON.stringify(activityFixture));
    localStorage.setItem('participant', JSON.stringify(ownerParticipantFixture));

    TestBed.configureTestingModule({
      providers: [
        ActivityFlowFacade,
        { provide: SubmitEvaluationUseCase, useValue: submitSpy },
        { provide: CloseActivityUserCase, useValue: closeSpy },
        { provide: Router, useValue: routerSpy },
      ],
    });

    facade = TestBed.inject(ActivityFlowFacade); 
  });

  afterEach(() => localStorage.clear());

  it('should submit only when participant is not owner', async () => {
    // WHEN
    await facade.execute(activityFixture, regularParticipantFixture, []);

    // THEN
    expect(submitSpy.execute).toHaveBeenCalledWith(activityFixture, regularParticipantFixture, []);
    expect(closeSpy.execute).not.toHaveBeenCalled();
    expect(localStorage.getItem('activity')).toEqual(JSON.stringify(activityFixture));
    expect(routerSpy.navigate).not.toHaveBeenCalled();
  });

  it('should close activity and navigate when participant is owner', async () => {
    // WHEN
    await facade.execute(activityFixture, ownerParticipantFixture, []);

    // THEN
    expect(closeSpy.execute).toHaveBeenCalledWith(activityFixture, ownerParticipantFixture);
    expect(localStorage.getItem('activity')).toBeNull();
    expect(localStorage.getItem('participant')).toBeNull();
    expect(routerSpy.navigate).toHaveBeenCalledWith([
      `activity/${activityFixture.activity_id}/result`,
    ]);
  });
});
