import { CommonModule } from '@angular/common';
import { Component, OnInit, OnDestroy, Inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatSliderModule } from '@angular/material/slider';
import { MatTabsModule } from '@angular/material/tabs';
import { RouterModule, Router } from '@angular/router';

import { isEqual } from 'lodash';

import { distinctUntilChanged, filter, map, Subscription, tap } from 'rxjs';

import {
  getActivityFromLocalStorage,
  getParticipantFromLocalStorage,
} from 'adapters/local-storage/utils';
import { ActivityStreamMessage } from 'application/dtos/activity-stream.dto';
import {
  ActivityStreamUseCasePort,
  ACTIVITY_STREAM_USE_CASE_PORT,
} from 'application/ports/activity-stream-use-case-port';
import { Activity, DimensionWithScores, Participant } from 'domain/model';

import { ControlActivityComponent } from './control-activity/control-activity.component';
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
    ControlActivityComponent,
  ],
})
export class ActivityComponent implements OnInit, OnDestroy {
  private subscription!: Subscription;

  activity: Activity | null = null;
  currentParticipant: Participant | null = null;
  dimensions: DimensionWithScores[] = [];
  participants: Participant[] = [];

  constructor(
    private readonly router: Router,
    @Inject(ACTIVITY_STREAM_USE_CASE_PORT)
    private readonly activityStreamUseCase: ActivityStreamUseCasePort
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

    this.subscription = this.activityStreamUseCase
      .startObserving(this.activity.activity_id, this.currentParticipant.id)
      .pipe(
        tap((msg: ActivityStreamMessage) => {
          if (!msg.is_opened) {
            const redirectTo = `activity/${msg.activity_id}/result`;
            this.router.navigate([redirectTo]);
          }
        }),
        filter((msg: ActivityStreamMessage) => msg.is_opened),
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
    this.activityStreamUseCase.stopObserving();
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }
}
