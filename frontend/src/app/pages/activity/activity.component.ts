import { Component, OnInit, OnDestroy } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSliderModule } from '@angular/material/slider';
import { distinctUntilChanged, map, Subscription } from 'rxjs';
import { isEqual } from 'lodash';

import { Activity, DimensionWithScores, Participant } from '@models/activity.model';
import { ActivityStreamMessage, ActivityStreamUseCase } from '@use-cases/activity-stream.usecase';
import { SubmitEvaluationService } from '@use-cases/submit-evaluation.usecase';
import { getActivityFromLocalStorage, getParticipantFromLocalStorage } from '@utils/utils';

import { EvaluationWrapperComponent } from './evaluation-wrapper/evaluation-wrapper.component';
import { ListParticipantsComponent } from './list-participants/list-participants.component';

@Component({
  selector: 'app-activity',
  templateUrl: './activity.component.html',
  standalone: true,
  imports: [
    RouterModule,
    CommonModule,
    FormsModule,
    MatCardModule,
    MatTabsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatSliderModule,
    EvaluationWrapperComponent,
    ListParticipantsComponent,
  ],
})
export class ActivityComponent implements OnInit, OnDestroy {
  private subscription!: Subscription;

  isSubmitting = false;

  activity: Activity | null = null;
  currentParticipant: Participant | null = null;
  dimensions: DimensionWithScores[] = [];
  participants: Participant[] = [];

  constructor(
    private readonly activityStreamService: ActivityStreamUseCase,
    private readonly submitEvaluationService: SubmitEvaluationService
  ) {}

  async ngOnInit() {
    this.activity = getActivityFromLocalStorage() as Activity;
    this.currentParticipant = getParticipantFromLocalStorage() as Participant;

    this.dimensions = this.activity.dimensions.map(dimension => ({
      ...dimension,
      principles: dimension.principles.map(principle => ({
        ...principle,
        score: 0,
      })),
    }));

    this.subscription = this.activityStreamService
      .startObserving(this.activity.activity_id, this.currentParticipant.id)
      .pipe(
        map((msg: ActivityStreamMessage) => msg.participants),
        distinctUntilChanged((prev, curr) => isEqual(prev, curr))
      )
      .subscribe({
        next: (msg: Participant[]) => {
          this.participants = msg;
        },
        error: (err: unknown) => console.error(err),
        complete: () => console.debug('[ActivityComponent] Activity stream finished'),
      });
  }

  ngOnDestroy() {
    this.activityStreamService.stopObserving();
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }

  async submit(): Promise<void> {
    this.isSubmitting = true;

    if (!this.activity || !this.currentParticipant) {
      throw new Error('[ActivityComponent] Activity or participant is not defined');
    }

    try {
      this.submitEvaluationService.submitEvaluation(
        this.activity,
        this.currentParticipant,
        this.dimensions
      );
    } catch (error) {
      console.error('[ActivityComponent]', error);
      this.isSubmitting = false;
    }
  }
}
