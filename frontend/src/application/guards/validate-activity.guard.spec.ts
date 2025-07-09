import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import { of } from 'rxjs';

import { AgileWheelBackEndHTTP } from 'adapters/http/agile-wheel-backend.http';
import {
  activityFixture,
  regularParticipantFixture,
  createRoute,
  mockLocalStorage,
} from 'testing/fixtures';

import { ValidateActitivityGuard } from './validate-activity.guard';

describe('ValidateActitivityGuard', () => {
  let guard: ValidateActitivityGuard;

  let routerSpy: jasmine.SpyObj<Router>;
  let httpSpy: jasmine.SpyObj<AgileWheelBackEndHTTP>;

  beforeEach(() => {
    routerSpy = jasmine.createSpyObj<Router>('Router', ['navigate']);
    httpSpy = jasmine.createSpyObj<AgileWheelBackEndHTTP>('AgileWheelBackEndHTTP', ['get']);

    TestBed.configureTestingModule({
      providers: [
        ValidateActitivityGuard,
        { provide: Router, useValue: routerSpy },
        { provide: AgileWheelBackEndHTTP, useValue: httpSpy },
      ],
    });

    guard = TestBed.inject(ValidateActitivityGuard);
  });

  afterEach(() => localStorage.clear());

  it('should redirect when id is missing', async () => {
    // GIVEN
    mockLocalStorage(activityFixture, regularParticipantFixture);

    // WHEN
    // eslint-disable-next-line sonarjs/no-undefined-argument
    const result = await guard.canActivate(createRoute(undefined)); // id is undefined

    // THEN
    expect(result).toBeFalse();
    expect(routerSpy.navigate).toHaveBeenCalledWith(['/create-activity']);
  });

  it('should redirect when localStorage data is missing', async () => {
    // GIVEN
    mockLocalStorage(null, null);

    // WHEN
    const result = await guard.canActivate(createRoute('a1'));

    // THEN
    expect(result).toBeFalse();
    expect(routerSpy.navigate).toHaveBeenCalledWith(['/create-activity']);
  });

  it('should redirect when activity id mismatches', async () => {
    // GIVEN
    mockLocalStorage(activityFixture, regularParticipantFixture);

    // WHEN
    const result = await guard.canActivate(createRoute('wrong'));

    // THEN
    expect(result).toBeFalse();
    expect(routerSpy.navigate).toHaveBeenCalledWith(['/create-activity']);
  });

  it('should redirect when backend returns invalid activity', async () => {
    // GIVEN
    mockLocalStorage(activityFixture, regularParticipantFixture);
    httpSpy.get.and.returnValue(of({ activity: { ...activityFixture, activity_id: 'x' } }));

    // WHEN
    const result = await guard.canActivate(createRoute('a1'));

    // THEN
    expect(result).toBeFalse();
    expect(routerSpy.navigate).toHaveBeenCalledWith(['/create-activity']);
  });

  it('should allow navigation when everything matches', async () => {
    // GIVEN
    mockLocalStorage(activityFixture, regularParticipantFixture);
    httpSpy.get.and.returnValue(of({ activity: activityFixture }));

    // WHEN
    const result = await guard.canActivate(createRoute('a1'));

    // THEN
    expect(result).toBeTrue();
  });
});
