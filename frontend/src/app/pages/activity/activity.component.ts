import { Component, OnInit } from '@angular/core';

import { RouterModule, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSliderModule } from '@angular/material/slider';

import { EvaluationWrapperComponent } from "./evaluation-wrapper/evaluation-wrapper.component";
import { ListParticipantsComponent } from './list-participants/list-participants.component';
import { Activity, Dimension, Participant } from '../../core/models/activity.model';

@Component({
  selector: 'app-activity',
  templateUrl: './activity.component.html',
  standalone: true,
  imports: [
    // Angular Core
    RouterModule,
    CommonModule,
    FormsModule,
    // Angular Material
    MatCardModule,
    MatTabsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatSliderModule,
    // App
    EvaluationWrapperComponent,
    ListParticipantsComponent
  ],
})
export class ActivityComponent  implements OnInit {
  dimensions: Dimension[] = [];
  participants: Participant[] = [];
  // values: Record<string, number> = {};

  ngOnInit() {
    const activity = localStorage.getItem('activity');

    if (activity) {
      const activityData:Activity = JSON.parse(activity);

      this.dimensions = activityData.dimensions;
      this.participants = activityData.participants;
    }
  }

  onSliderChange(label: string, event: Event) {
    const input = event.target as HTMLInputElement;
    // this.values[label] = parseInt(input.value, 10) || 0;
  }

  canSubmit(): boolean {
    return true;
  }

  submit() {
    if (!this.canSubmit()) { return; }
    // console.log('Enviar respostas:', this.values);
  }

}
