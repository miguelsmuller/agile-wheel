import { TestBed } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';

import { of } from 'rxjs';

import { ECHARTS_TOKEN } from 'adapters/echarts/echarts.token';
import { GetActivityResultResponse } from 'application/dtos/get-activity-result.dto';
import {
  GET_ACTIVITY_RESULT_USE_CASE_PORT,
  GetActivityResultUseCasePort,
} from 'application/ports/get-activity-result-use-case-port';

import { ResultComponent } from './result.component';

describe('ResultComponent', () => {
  let useCaseSpy: jasmine.SpyObj<GetActivityResultUseCasePort>;
  let routeParam: string | null;
  let echartsStub: { init: jasmine.Spy; use: jasmine.Spy };

  beforeEach(async () => {
    useCaseSpy = jasmine.createSpyObj<GetActivityResultUseCasePort>(
      'GetActivityResultUseCasePort',
      ['execute']
    );
    routeParam = 'a1';
    const chartStub = { setOption: jasmine.createSpy('setOption') };


    echartsStub = {
      init: jasmine.createSpy('init').and.returnValue(chartStub as any),
      use: jasmine.createSpy('use'),
    };

    await TestBed.configureTestingModule({
      imports: [ResultComponent],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: { snapshot: { paramMap: { get: () => routeParam } } },
        },
        { provide: GET_ACTIVITY_RESULT_USE_CASE_PORT, useValue: useCaseSpy },
        { provide: ECHARTS_TOKEN, useValue: echartsStub },
      ],
    }).compileComponents();
  });

  it('should fetch result on init', () => {
    const response: GetActivityResultResponse = {
      activity: { activity_id: 'a1', created_at: 'now', is_opened: false },
      result: { overall_score: 0, dimension_scores: [] },
    };
    useCaseSpy.execute.and.returnValue(of(response));

    const fixture = TestBed.createComponent(ResultComponent);
    const component = fixture.componentInstance;

    component.ngOnInit();

    expect(useCaseSpy.execute).toHaveBeenCalledWith('a1');
    expect(component.result).toEqual(response.result);
  });

  it('should not fetch when id is missing', () => {
    routeParam = null;
    const fixture = TestBed.createComponent(ResultComponent);
    const component = fixture.componentInstance;

    component.ngOnInit();

    expect(useCaseSpy.execute).not.toHaveBeenCalled();
  });
});
