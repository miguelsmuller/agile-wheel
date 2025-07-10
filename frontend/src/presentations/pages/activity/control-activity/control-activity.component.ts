import { CommonModule } from '@angular/common';
import { Component, Input, Inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { RouterModule } from '@angular/router';

import {
  ActivityFlowUseCasePort,
  ACTIVITY_FLOW_USE_CASE_PORT,
} from 'application/ports/activity-flow-use-case-port';
import { Activity, DimensionWithScores, Participant } from 'domain/model';

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

  constructor(
    @Inject(ACTIVITY_FLOW_USE_CASE_PORT)
    private readonly activityFlowUseCase: ActivityFlowUseCasePort
  ) {}

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
      await this.activityFlowUseCase.execute(
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
