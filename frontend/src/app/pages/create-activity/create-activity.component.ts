import { Component, OnInit } from '@angular/core';
import { RouterModule, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { CreateActivityService, CreateActivityRequest } from '../../use-cases/create-activity.usecase';
import { Activity } from '../../models/activity.model';


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
export class CreateActivityComponent implements OnInit {
  createForm: FormGroup;
  isSubmitting: boolean = false;

  constructor(
    private formBuilder: FormBuilder,
    private createActivityService: CreateActivityService,
    private router: Router
  ) {
    this.createForm = this.formBuilder.group({
      name: ['', Validators.required],
      email: ['', [
        Validators.required, 
        Validators.email
      ]],
    });
  }

  ngOnInit(): void {
    const activity = localStorage.getItem('activity');

    if (activity) {
      const activityData:Activity = JSON.parse(activity);
      this.router.navigate(['/activity', activityData.activity_id]);
    }
  }

  async createActivity(): Promise<void> {
    if (this.createForm.invalid) return;

    this.isSubmitting = true;
    
    const owner: CreateActivityRequest = {
      email: this.createForm.value.email,
      name: this.createForm.value.name
    };

    try {
      await this.createActivityService.createActivity(owner);
    } catch (error) {
      console.error('[createActivity]', error);
      this.isSubmitting = false;
    }
  }
}