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
import { Participant } from '@models/activity.model';

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
