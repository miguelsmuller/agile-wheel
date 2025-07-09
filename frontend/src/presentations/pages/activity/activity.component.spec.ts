import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import { Subject } from 'rxjs';

import { ActivityStreamMessage } from 'application/dtos/activity-stream.dto';
import {
  ACTIVITY_FLOW_USE_CASE_PORT,
  ActivityFlowUseCasePort,
} from 'application/ports/activity-flow-use-case-port';
import {
  ACTIVITY_STREAM_USE_CASE_PORT,
  ActivityStreamUseCasePort,
} from 'application/ports/activity-stream-use-case-port';
import { Activity, Participant } from 'domain/model';
import { activityFixture, regularParticipantFixture, dimensionsFixture } from 'testing/fixtures';

import { ActivityComponent } from './activity.component';

const activity: Activity = {
  ...activityFixture,
  dimensions: dimensionsFixture,
};
const participant: Participant = regularParticipantFixture;

describe('ActivityComponent', () => {
  let component: ActivityComponent;

  let stream$: Subject<ActivityStreamMessage>;

  let streamUseCaseSpy: jasmine.SpyObj<ActivityStreamUseCasePort>;
  let flowUseCaseSpy: jasmine.SpyObj<ActivityFlowUseCasePort>;
  let routerSpy: jasmine.SpyObj<Router>;

  beforeEach(async () => {
    stream$ = new Subject<ActivityStreamMessage>();

    streamUseCaseSpy = jasmine.createSpyObj<ActivityStreamUseCasePort>(
      'ActivityStreamUseCasePort',
      ['startObserving', 'stopObserving']
    );
    streamUseCaseSpy.startObserving.and.returnValue(stream$.asObservable());

    flowUseCaseSpy = jasmine.createSpyObj<ActivityFlowUseCasePort>('ActivityFlowUseCasePort', [
      'execute',
    ]);

    routerSpy = jasmine.createSpyObj<Router>('Router', ['navigate']);

    localStorage.setItem('activity', JSON.stringify(activity));
    localStorage.setItem('participant', JSON.stringify(participant));

    await TestBed.configureTestingModule({
      imports: [ActivityComponent], // standalone
      providers: [
        { provide: ACTIVITY_STREAM_USE_CASE_PORT, useValue: streamUseCaseSpy },
        { provide: ACTIVITY_FLOW_USE_CASE_PORT, useValue: flowUseCaseSpy },
        { provide: Router, useValue: routerSpy },
      ],
    }).compileComponents();

    component = TestBed.createComponent(ActivityComponent).componentInstance;
  });

  afterEach(() => {
    localStorage.clear();
    stream$.complete();
  });

  it('should initialize dimension scores with zero', async () => {
    // WHEN
    await component.ngOnInit();

    // THEN
    expect(component.dimensions[0].principles[0].score).toBe(0);
  });

  it('should update participants when stream emits', async () => {
    // GIVEN
    await component.ngOnInit();
    const msg: ActivityStreamMessage = {
      activity_id: 'a1',
      created_at: 'now',
      is_opened: true,
      participants: [{ id: 'p2', name: 'x', email: 'e' }],
    };

    // WHEN
    stream$.next(msg);

    // THEN
    expect(component.participants).toEqual(msg.participants);
  });

  it('should navigate when activity closes', async () => {
    // GIVEN
    await component.ngOnInit();
    const msg: ActivityStreamMessage = {
      activity_id: 'a1',
      created_at: 'now',
      is_opened: false,
      participants: [],
    };

    // WHEN
    stream$.next(msg);

    // THEN
    expect(routerSpy.navigate).toHaveBeenCalledWith(['activity/a1/result']);
  });

  it('should stop observing on destroy', async () => {
    // GIVEN
    await component.ngOnInit();

    // WHEN
    component.ngOnDestroy();

    // THEN
    expect(streamUseCaseSpy.stopObserving).toHaveBeenCalled();
  });
});
