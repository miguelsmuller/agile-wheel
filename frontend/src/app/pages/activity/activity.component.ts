import { Component, OnInit } from '@angular/core';
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

import { EvaluationWrapperComponent } from "./evaluation-wrapper/evaluation-wrapper.component";
import { ListParticipantsComponent } from './list-participants/list-participants.component';

@Component({
  selector: 'app-activity',
  templateUrl: './activity.component.html',
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
    // App
    EvaluationWrapperComponent,
    ListParticipantsComponent
  ],
})
export class ActivityComponent  implements OnInit {
  groups: Record<string, string[]> = {
    'Pessoas Sensacionais': [
      'Colaboração e comunicação',
      'Motivação e confiança',
      'Autonomia e auto-organização',
      'Melhoria Contínua',
      'Interdisciplinaridade',
    ],
    'Experimente e Aprenda Rápido': [
      'Compartilhamento de conhecimento',
      'Comprometimento com o produto',
      'Práticas Lean-Agile',
      'Ritmo das entregas',
      'Granularidade de demandas',
    ],
    'Segurança é um Pré-requisito': [
      'Trabalho sustentável',
      'Métricas Ágeis',
      'Estimativas & contratos ágeis',
      'Metas/OKRs',
      'Desdobramentos estratégicos',
    ],
    'Valor a Todo Instante': [
      'Discovery/Upstream Kanban',
      'User Experience (UX/UI)',
      'Entrega de valor (percebido)',
      'Relacionamento com o negócio',
      'Satisfação do cliente',
    ],
  };

  participants = [
    {
      name: 'Leslie Alexander',
      role: 'Co-Founder / CEO',
      avatarUrl: 'https://i.pravatar.cc/100?img=1'
    },
    {
      name: 'Jacob Jones',
      role: 'Product Manager',
      avatarUrl: 'https://i.pravatar.cc/100?img=2'
    },
    {
      name: 'Cody Fisher',
      role: 'Tech Lead',
      avatarUrl: 'https://i.pravatar.cc/100?img=3'
    },
    {
      name: 'Jenny Wilson',
      role: 'UX Designer',
      avatarUrl: 'https://i.pravatar.cc/100?img=4'
    },
    {
      name: 'Marvin McKinney',
      role: 'DevOps Engineer',
      avatarUrl: 'https://i.pravatar.cc/100?img=5'
    },
    {
      name: 'Jacob Jones',
      role: 'Product Manager',
      avatarUrl: 'https://i.pravatar.cc/100?img=2'
    },
    {
      name: 'Cody Fisher',
      role: 'Tech Lead',
      avatarUrl: 'https://i.pravatar.cc/100?img=3'
    },
    {
      name: 'Jenny Wilson',
      role: 'UX Designer',
      avatarUrl: 'https://i.pravatar.cc/100?img=4'
    },
    {
      name: 'Marvin McKinney',
      role: 'DevOps Engineer',
      avatarUrl: 'https://i.pravatar.cc/100?img=5'
    },
    {
      name: 'Jacob Jones',
      role: 'Product Manager',
      avatarUrl: 'https://i.pravatar.cc/100?img=2'
    },
    {
      name: 'Cody Fisher',
      role: 'Tech Lead',
      avatarUrl: 'https://i.pravatar.cc/100?img=3'
    },
    {
      name: 'Jenny Wilson',
      role: 'UX Designer',
      avatarUrl: 'https://i.pravatar.cc/100?img=4'
    },
    {
      name: 'Marvin McKinney',
      role: 'DevOps Engineer',
      avatarUrl: 'https://i.pravatar.cc/100?img=5'
    },
    {
      name: 'Jacob Jones',
      role: 'Product Manager',
      avatarUrl: 'https://i.pravatar.cc/100?img=2'
    },
    {
      name: 'Cody Fisher',
      role: 'Tech Lead',
      avatarUrl: 'https://i.pravatar.cc/100?img=3'
    },
    {
      name: 'Jenny Wilson',
      role: 'UX Designer',
      avatarUrl: 'https://i.pravatar.cc/100?img=4'
    },
    {
      name: 'Marvin McKinney',
      role: 'DevOps Engineer',
      avatarUrl: 'https://i.pravatar.cc/100?img=5'
    }
  ];


  values: Record<string, number> = {};

  ngOnInit() {
    Object.values(this.groups)
      .flat()
      .forEach(label => (this.values[label] = 0));
    this.calcRemaining();
  }

  onSliderChange(label: string, event: Event) {
    const input = event.target as HTMLInputElement;
    this.values[label] = parseInt(input.value, 10) || 0;
    this.calcRemaining();
  }

  private calcRemaining() {
    const used = Object.values(this.values).reduce((sum, v) => sum + v, 0);
  }

  canSubmit(): boolean {
    return true;
  }

  submit() {
    if (!this.canSubmit()) { return; }
    console.log('Enviar respostas:', this.values);
  }

}
