import { Component, Input } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { Activity, DimensionWithScores, Participant } from '@models/activity.model';
import { ActivityFlowFacade } from '@use-cases/activity-flow.facade';

@Component({
  selector: 'app-control-activity',
  templateUrl: './control-activity.component.html',
  standalone: true,
  imports: [
    RouterModule,
    CommonModule,
    FormsModule,
    MatCardModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
  ],
})
export class ControlActivityComponent {
  isSubmitting = false;

  @Input() activity!: Activity;
  @Input() currentParticipant!: Participant;
  @Input() dimensions!: DimensionWithScores[];

  constructor(private readonly activityFlow: ActivityFlowFacade) {}

  get buttonLabel(): string {
    if (this.activity?.owner?.id === this.currentParticipant?.id) {
      return this.isSubmitting ? 'Enviando...' : 'Enviar e Concluir';
    }
    return this.isSubmitting ? 'Enviando...' : 'Enviar Respostas';
  }

  async submit(): Promise<void> {
    this.isSubmitting = true;

    if (!this.activity || !this.currentParticipant) {
      throw new Error('[ActivityComponent] Activity or participant is not defined');
    }

    try {
      await this.activityFlow.submitActivityFlow(
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
