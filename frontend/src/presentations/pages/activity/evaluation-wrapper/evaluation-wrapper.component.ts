import { Component, Input } from '@angular/core';
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

import { DimensionWithScores } from 'domain/model';

import { EvaluationItensComponent } from '../evaluation-itens/evaluation-itens.component';

@Component({
  selector: 'app-evaluation-wrapper',
  templateUrl: './evaluation-wrapper.component.html',
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
    EvaluationItensComponent,
  ],
})
export class EvaluationWrapperComponent {
  @Input() dimensions!: DimensionWithScores[];
}
