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

import { Participant } from 'domain/model';

@Component({
  selector: 'app-list-participants',
  templateUrl: './list-participants.component.html',
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
  ],
})
export class ListParticipantsComponent {
  @Input() participants!: Participant[];

  trackById(index: number, participant: Participant): string {
    return participant.id;
  }
}
