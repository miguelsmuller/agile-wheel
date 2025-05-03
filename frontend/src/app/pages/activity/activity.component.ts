import { Component, OnInit } from '@angular/core';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSliderModule } from '@angular/material/slider';
import { distinctUntilChanged, map, Subscription, tap } from 'rxjs';
import { isEqual } from 'lodash';


import { EvaluationWrapperComponent } from "./evaluation-wrapper/evaluation-wrapper.component";
import { ListParticipantsComponent } from './list-participants/list-participants.component';
import { Activity, Dimension, Participant } from '../../models/activity.model';
import { ActivityStateService } from '../../use-cases/validate-activity.usecase';
import { ActivityStreamUseCase } from '../../use-cases/activity-stream.usecase';

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
    ListParticipantsComponent
  ],
})
export class ActivityComponent  implements OnInit {
  private sub!: Subscription;

  activity: Activity | null = null;
  currentParticipant: Participant | null = null;
  dimensions: Dimension[] = [];
  participants: Participant[] = [];
  values: Record<string, number> = {};

  constructor(
    private activatedRoute: ActivatedRoute,
    private activityStateService: ActivityStateService,
    private activityStreamService: ActivityStreamUseCase
  ) {}

  async ngOnInit() {
    const activityId = this.activatedRoute.snapshot.paramMap.get('id');
    if (!activityId) return;

    const { activity, currentParticipant } = await this.activityStateService.initialize(activityId);
    this.activity = activity;
    this.currentParticipant = currentParticipant;

    this.dimensions = activity.dimensions;
    this.dimensions.forEach(dimension => {
      dimension.principles.forEach(principle => {
        this.values[principle.id] = 0;
      });
    });

    this.sub = this.activityStreamService.startObserving(
      activity.activity_id,
      currentParticipant.id
    ).pipe(
      map((msg: any) => msg.participants),
      distinctUntilChanged((prev, curr) => isEqual(prev, curr))
    ).subscribe({
      next: (msg: Participant[]) => {
        this.participants = msg;
      },
      error: (err: any) => console.error(err),
      complete: () => console.debug('activity stream finished')
    });
  }

  ngOnDestroy() {
    this.activityStreamService.stopObserving();
    this.sub.unsubscribe();
  }

  onSliderChange(label: string, event: Event) {
    const input = event.target as HTMLInputElement;
    this.values[label] = parseInt(input.value, 10) || 0;
  }

  submit() {
    console.log('Enviar respostas:', this.values);
  }  
}
