import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  imports: [
    RouterModule,
  ]
})
export class HomeComponent {
  dynamicId: string = '';
  name: string = '';
  email: string = '';

  joinDynamic() {
    // Implementar lógica para entrar em uma dinâmica
    console.log('Entrar na dinâmica:', this.dynamicId, this.name, this.email);
  }

  createDynamic() {
    // Implementar lógica para criar uma dinâmica
    console.log('Criar dinâmica:', this.name, this.email);
  }
}