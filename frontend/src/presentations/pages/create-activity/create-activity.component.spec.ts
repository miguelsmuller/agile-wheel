import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';

import { of, throwError } from 'rxjs';

import { CreateActivityResponse } from 'application/dtos/create-activity.dto';
import {
  CREATE_ACTIVITY_USE_CASE_PORT,
  CreateActivityUseCasePort,
} from 'application/ports/create-activity-use-case-port';
import { Activity, Participant } from 'domain/model';

import { CreateActivityComponent } from './create-activity.component';

describe('CreateActivityComponent', () => {
  let component: CreateActivityComponent;

  let useCaseSpy: jasmine.SpyObj<CreateActivityUseCasePort>;

  let routeParam: string | null;

  beforeEach(async () => {
    useCaseSpy = jasmine.createSpyObj<CreateActivityUseCasePort>('CreateActivityUseCasePort', [
      'execute',
    ]);

    routeParam = null;

    await TestBed.configureTestingModule({
      imports: [CreateActivityComponent],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: { snapshot: { paramMap: { get: () => routeParam } } },
        },
        { provide: CREATE_ACTIVITY_USE_CASE_PORT, useValue: useCaseSpy },
      ],
    }).compileComponents();

    component = TestBed.createComponent(CreateActivityComponent).componentInstance;
  });

  afterEach(() => localStorage.clear());

  it('should execute use case when form is valid', async () => {
    // Given
    const response: CreateActivityResponse = {
      participant: {} as Participant,
      activity: {} as Activity,
    };

    useCaseSpy.execute.and.returnValue(of(response));

    component.createForm.setValue({ name: 'John', email: 'j@x' });

    // When
    await component.createActivity();

    // Then
    expect(useCaseSpy.execute).toHaveBeenCalledWith({ name: 'John', email: 'j@x' });
    expect(component.isSubmitting).toBeTrue();
  });

  it('should not execute use case when form is invalid', async () => {
    // Given
    component.createForm.patchValue({ name: 'John' });

    // When
    await component.createActivity();

    // Then
    expect(useCaseSpy.execute).not.toHaveBeenCalled();
  });

  it('should reset submitting flag when use case errors', fakeAsync(() => {
    // Given
    useCaseSpy.execute.and.returnValue(throwError(() => new Error('fail')));

    component.createForm.setValue({ name: 'John', email: 'j@x' });

    // When
    component.createActivity();

    tick();

    // Then
    expect(component.isSubmitting).toBeFalse();
  }));
});
