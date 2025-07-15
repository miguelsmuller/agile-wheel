import { Component, Inject, OnInit } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { ActivatedRoute } from '@angular/router';

import {
  GET_ACTIVITY_RESULT_USE_CASE_PORT,
  GetActivityResultUseCasePort,
} from 'application/ports/get-activity-result-use-case-port';
import { ActivityResult } from 'domain/model';

import { ChartResultComponent } from './chart-result/chart-result.component';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  standalone: true,
  imports: [MatIconModule, ChartResultComponent],
})
export class ResultComponent implements OnInit {
  result: ActivityResult | null = null;

  constructor(
    private readonly route: ActivatedRoute,
    @Inject(GET_ACTIVITY_RESULT_USE_CASE_PORT)
    private readonly getResultUseCase: GetActivityResultUseCasePort
  ) {}

  ngOnInit(): void {
    const activityId = this.route.snapshot.paramMap.get('id');

    if (!activityId) return;

    this.getResultUseCase.execute(activityId).subscribe({
      next: response => (this.result = response.result),
      error: err => console.error('[ResultComponent] Failed to load result', err),
    });
  }
}
