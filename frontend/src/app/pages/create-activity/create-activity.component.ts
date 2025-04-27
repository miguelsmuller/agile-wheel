import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { CreateActivityService, CreateActivityRequest } from '../../core/use-cases/create-activity.usecase';


@Component({
  selector: 'app-create-activity',
  templateUrl: './create-activity.component.html',
  standalone: true,
  imports: [
    // Angular
    ReactiveFormsModule,
    RouterModule,
    // Angular Material
    MatCardModule,
    MatTabsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule
  ],
})
export class CreateActivityComponent {
  createForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private createActivityService: CreateActivityService
  ) {
    this.createForm = this.formBuilder.group({
      name: ['', Validators.required],
      email: ['', [
        Validators.required, 
        Validators.email
      ]],
    });
  }

  createActivity(): void {
    if (this.createForm.invalid) return;
    
    const owner: CreateActivityRequest = {
      owner_email: this.createForm.value.email,
      owner_name: this.createForm.value.name
    };

    this.createActivityService.createActivity(owner);
  }
}