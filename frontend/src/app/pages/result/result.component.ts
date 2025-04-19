import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  standalone: true,
  imports: [
    RouterModule,
    MatButtonModule,
  ],
})
export class ResultComponent {
  // Implementar lógica de interação da dinâmica
}