import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

import { ChartResultComponent } from './chart-result/chart-result.component';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  standalone: true,
  imports: [MatIconModule, ChartResultComponent],
})
export class ResultComponent {}
