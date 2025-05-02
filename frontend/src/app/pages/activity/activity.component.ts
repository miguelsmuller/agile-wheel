import { Component, OnInit, OnDestroy } from '@angular/core';
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
import { Subscription } from 'rxjs';

import { EvaluationWrapperComponent } from "./evaluation-wrapper/evaluation-wrapper.component";
import { ListParticipantsComponent } from './list-participants/list-participants.component';
import { Activity, Dimension, Participant } from '../../models/activity.model';
import { ValidateActivityService } from '../../use-cases/validate-activity.usecase';
import { ActivityStreamUseCase } from '../../use-cases/activity-stream';

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
  private sub!: Subscription;

  activity: Activity | null = null;
  dimensions: Dimension[] = [];
  participants: Participant[] = [];
  values: Record<string, number> = {};

  constructor(
    private activatedRoute: ActivatedRoute,
    private validateActivity: ValidateActivityService,
    private activityStatus: ActivityStreamUseCase
    
  ) {}

  async ngOnInit() {
    const activityIdFromURL = this.activatedRoute.snapshot.paramMap.get('id');
    this.activity = await this.validateActivity.validate(activityIdFromURL as string)

    this.dimensions = this.activity.dimensions; 
    this.participants = this.activity.participants;
    this.dimensions.forEach(dimension => {
      dimension.principles.forEach(principle => {
        this.values[principle.id] = 0;
      });
    });

    this.sub = this.activityStatus.observeStatus().subscribe({
      next: (msg) => console.log('Recebido:', msg.value),
      error: (err) => console.error('Erro:', err),
      complete: () => console.log('Finalizado')
    });
  }

  ngOnDestroy() {
    this.activityStatus.stopObserving();
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
