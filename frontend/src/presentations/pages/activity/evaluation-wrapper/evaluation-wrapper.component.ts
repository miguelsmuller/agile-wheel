import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatSliderModule } from '@angular/material/slider';
import { MatTabsModule } from '@angular/material/tabs';
import { RouterModule } from '@angular/router';

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
