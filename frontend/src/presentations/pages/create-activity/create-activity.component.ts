import { Component } from '@angular/core';
import { Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatTabsModule } from '@angular/material/tabs';
import { RouterModule } from '@angular/router';

import { CreateActivityRequest } from 'application/dtos/create-activity.dto';
import {
  CreateActivityUseCasePort,
  CREATE_ACTIVITY_USE_CASE_PORT,
} from 'application/ports/create-activity-use-case-port';

@Component({
  selector: 'app-create-activity',
  templateUrl: './create-activity.component.html',
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
export class CreateActivityComponent {
  createForm: FormGroup;
  isSubmitting = false;

  constructor(
    private readonly formBuilder: FormBuilder,
    @Inject(CREATE_ACTIVITY_USE_CASE_PORT)
    private readonly createActivityUseCase: CreateActivityUseCasePort
  ) {
    this.createForm = this.formBuilder.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
    });
  }

  async createActivity(): Promise<void> {
    if (this.createForm.invalid) return;

    this.isSubmitting = true;

    const owner: CreateActivityRequest = {
      email: this.createForm.value.email,
      name: this.createForm.value.name,
    };

    this.createActivityUseCase.execute(owner).subscribe({
      next: () => console.log('[createActivity] Activity created successfully'),
      error: error => {
        this.isSubmitting = false;
        console.error('[createActivity]', error);
      },
    });
  }
}
