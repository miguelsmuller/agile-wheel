import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-enter-activity',
  templateUrl: './enter-activity.component.html',
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
    MatIconModule,
  ],
})
export class EnterActivityComponent {
  createForm: FormGroup;
  joinForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.createForm = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
    });

    this.joinForm = this.fb.group({
      id: ['', Validators.required],
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
    });
  }

  /** Handler para gerar nova dinâmica */
  onCreate(): void {
    if (this.createForm.invalid) return;
    console.info('Criar atividade', this.createForm.value);
    // TODO: integrar com endpoint POST /activity/create
  }

  /** Handler para entrar em dinâmica existente */
  onJoin(): void {
    if (this.joinForm.invalid) return;
    console.info('Entrar na atividade', this.joinForm.value);
    // TODO: integrar com endpoint GET /activity/{id}
  }
}
