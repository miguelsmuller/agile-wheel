import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';

import { of, throwError } from 'rxjs';

import { EnterActivityResponse } from 'application/dtos/enter-activity.dto';
import {
  ENTER_ACTIVITY_USE_CASE_PORT,
  EnterActivityUseCasePort,
} from 'application/ports/enter-activity-use-case-port';
import { Activity, Participant } from 'domain/model';

import { EnterActivityComponent } from './enter-activity.component';

describe('EnterActivityComponent', () => {
  let component: EnterActivityComponent;

  let useCaseSpy: jasmine.SpyObj<EnterActivityUseCasePort>;

  let routeParam: string | null;

  beforeEach(async () => {
    useCaseSpy = jasmine.createSpyObj<EnterActivityUseCasePort>('EnterActivityUseCasePort', [
      'execute',
    ]);

    routeParam = null;

    await TestBed.configureTestingModule({
      imports: [EnterActivityComponent],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: { snapshot: { paramMap: { get: () => routeParam } } },
        },
        { provide: ENTER_ACTIVITY_USE_CASE_PORT, useValue: useCaseSpy },
      ],
    }).compileComponents();

    component = TestBed.createComponent(EnterActivityComponent).componentInstance;
  });

  afterEach(() => localStorage.clear());

  it('should prefill and disable id when route param exists', () => {
    // Given
    routeParam = 'a1';

    // When
    component.ngOnInit();

    // Then
    const control = component.enterForm.get('activityId');
    expect(control?.value).toBe('a1');
    expect(control?.disabled).toBeTrue();
  });

  it('should enable id field when route param is missing', () => {
    // Given
    routeParam = null;

    // When
    component.ngOnInit();

    // Then
    const control = component.enterForm.get('activityId');
    expect(control?.enabled).toBeTrue();
  });

  it('should execute use case when form is valid', async () => {
    // Given
    const response: EnterActivityResponse = {
      participant: {} as Participant,
      activity: {} as Activity,
    };

    useCaseSpy.execute.and.returnValue(of(response));

    component.enterForm.setValue({
      activityId: 'a1',
      participantName: 'John',
      participantEmail: 'j@x',
    });

    // When
    await component.enterActivity();

    // Then
    expect(useCaseSpy.execute).toHaveBeenCalledWith('a1', { name: 'John', email: 'j@x' });
    expect(component.isSubmitting).toBeTrue();
  });

  it('should not execute use case when form is invalid', async () => {
    // Given
    component.enterForm.patchValue({ participantName: 'John' });

    // When
    await component.enterActivity();

    // Then
    expect(useCaseSpy.execute).not.toHaveBeenCalled();
  });

  it('should reset submitting flag when use case errors', fakeAsync(() => {
    // Given
    useCaseSpy.execute.and.returnValue(throwError(() => new Error('fail')));

    component.enterForm.setValue({
      activityId: 'a1',
      participantName: 'John',
      participantEmail: 'j@x',
    });

    // When
    component.enterActivity();

    tick();

    // Then
    expect(component.isSubmitting).toBeFalse();
  }));
});
