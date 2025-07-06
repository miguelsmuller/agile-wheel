import { Routes } from '@angular/router';
import { ResultComponent } from './pages/result/result.component';
import { ActivityComponent } from './pages/activity/activity.component';
import { CreateActivityComponent } from './pages/create-activity/create-activity.component';
import { EnterActivityComponent } from './pages/enter-activity/enter-activity.component';
import { InitialStepGuard } from '../application/guards/initial-step.guard';
import { ValidateActitivityGuard } from '../application/guards/validate-activity.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'create-activity', pathMatch: 'full' },
  {
    path: 'create-activity',
    component: CreateActivityComponent,
    canActivate: [InitialStepGuard],
  },
  {
    path: 'enter-activity/:id',
    component: EnterActivityComponent,
    canActivate: [InitialStepGuard],
  },
  {
    path: 'enter-activity',
    component: EnterActivityComponent,
    canActivate: [InitialStepGuard],
  },
  {
    path: 'activity/:id',
    component: ActivityComponent,
    canActivate: [ValidateActitivityGuard],
  },
  {
    path: 'activity/:id/result',
    component: ResultComponent,
    canActivate: [],
  },
  { path: '**', redirectTo: 'create-activity' },
];
