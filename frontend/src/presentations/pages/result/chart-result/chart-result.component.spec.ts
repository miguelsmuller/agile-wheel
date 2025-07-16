import { SimpleChange } from '@angular/core';
import { TestBed } from '@angular/core/testing';

import { ECHARTS_TOKEN } from 'adapters/echarts/echarts.token';
import { ActivityResult } from 'domain/model';

import { ChartResultComponent } from './chart-result.component';

function createResult(): ActivityResult {
  return {
    overall_score: 0,
    dimension_scores: [
      {
        dimension: { id: 'd1', name: 'D1', comments: '', principles: [] },
        average_score: 1,
        total_ratings: 1,
        principles: [
          {
            principle: { id: 'p1', name: 'P1', comments: '' },
            average_score: 3,
            total_ratings: 1,
          },
        ],
      },
    ],
  };
}

describe('ChartResultComponent', () => {
  let chartSpy: { setOption: jasmine.Spy };
  let echartsStub: { init: jasmine.Spy; use: jasmine.Spy };

  beforeEach(async () => {
    chartSpy = { setOption: jasmine.createSpy('setOption') };

    echartsStub = {
      init: jasmine.createSpy('init').and.returnValue(chartSpy as any),
      use: jasmine.createSpy('use'),
    };

    await TestBed.configureTestingModule({
      imports: [ChartResultComponent],
      providers: [{ provide: ECHARTS_TOKEN, useValue: echartsStub }],
    }).compileComponents();
  });

  it('should init chart with result on view init', () => {
    const fixture = TestBed.createComponent(ChartResultComponent);
    const component = fixture.componentInstance;

    component.result = createResult();

    fixture.detectChanges();

    expect(chartSpy.setOption).toHaveBeenCalled();
  });

  it('should update chart when result changes', () => {
    const fixture = TestBed.createComponent(ChartResultComponent);
    const component = fixture.componentInstance;

    component.result = createResult();
    fixture.detectChanges();

    chartSpy.setOption.calls.reset();

    const newResult = createResult();

    component.ngOnChanges({
      result: new SimpleChange(component.result, newResult, false),
    });

    component.result = newResult;

    expect(chartSpy.setOption).toHaveBeenCalled();
  });
});
