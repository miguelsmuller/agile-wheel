import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';

import { InitialStepGuard } from './initial-step.guard';

describe('InitialStepGuard', () => {
  let guard: InitialStepGuard;
  let routerSpy: jasmine.SpyObj<Router>;

  beforeEach(() => {
    routerSpy = jasmine.createSpyObj<Router>('Router', ['navigate']);

    TestBed.configureTestingModule({
      providers: [InitialStepGuard, { provide: Router, useValue: routerSpy }],
    });

    guard = TestBed.inject(InitialStepGuard);
  });

  it('should permit navigation when no activity exists in localStorage', () => {
    // WHEN
    spyOn(localStorage, 'getItem').and.returnValue(null);

    // THEN
    expect(guard.canActivate()).toBeTrue();
  });

  it('should redirect to /activity/:id and return false when activity exists', () => {
    // WHEN
    spyOn(localStorage, 'getItem').and.returnValue(JSON.stringify({ activity_id: '123' }));

    // THEN
    expect(guard.canActivate()).toBeFalse();
    expect(routerSpy.navigate).toHaveBeenCalledWith(['/activity', '123']);
  });
});
