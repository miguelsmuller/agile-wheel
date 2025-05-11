import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { CreateActivityService, CreateActivityRequest } from '@use-cases/create-activity.usecase';

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
    private readonly createActivityService: CreateActivityService
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

    try {
      this.createActivityService.createActivity(owner);
    } catch (error) {
      console.error('[createActivity]', error);
      this.isSubmitting = false;
    }
  }
}
