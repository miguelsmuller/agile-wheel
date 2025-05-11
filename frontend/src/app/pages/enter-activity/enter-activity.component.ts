import { Component, OnInit } from '@angular/core';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { EnterActivityRequest, EnterActivityService } from '@use-cases/enter-activity.usecase';

@Component({
  selector: 'app-enter-activity',
  templateUrl: './enter-activity.component.html',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    RouterModule,
    MatCardModule,
    MatTabsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
  ],
})
export class EnterActivityComponent implements OnInit {
  enterForm: FormGroup;
  isSubmitting = false;

  constructor(
    private readonly activatedRoute: ActivatedRoute,
    private readonly formBuilder: FormBuilder,
    private readonly joinActivityService: EnterActivityService
  ) {
    this.enterForm = this.formBuilder.group({
      activityId: ['', Validators.required],
      participantName: ['', Validators.required],
      participantEmail: ['', [Validators.required, Validators.email]],
    });
  }

  ngOnInit(): void {
    const activityId = this.activatedRoute.snapshot.paramMap.get('id');

    if (activityId) {
      this.enterForm.patchValue({ activityId });
      this.enterForm.get('activityId')?.disable();
    } else {
      this.enterForm.get('activityId')?.enable();
    }
  }

  async enterActivity(): Promise<void> {
    if (this.enterForm.invalid) return;

    this.isSubmitting = true;

    const activityId = this.enterForm.get('activityId')?.value;
    const participant: EnterActivityRequest = {
      email: this.enterForm.get('participantEmail')?.value,
      name: this.enterForm.get('participantName')?.value,
    };

    try {
      this.joinActivityService.enterActivity(activityId, participant);
    } catch (error) {
      console.error('[enterActivity]', error);
      this.isSubmitting = false;
    }
  }
}
