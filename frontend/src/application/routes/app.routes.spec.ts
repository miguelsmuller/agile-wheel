import { InitialStepGuard } from 'application/guards/initial-step.guard';
import { ValidateActitivityGuard } from 'application/guards/validate-activity.guard';
import { ActivityComponent } from 'presentations/pages/activity/activity.component';
import { CreateActivityComponent } from 'presentations/pages/create-activity/create-activity.component';
import { EnterActivityComponent } from 'presentations/pages/enter-activity/enter-activity.component';
import { ResultComponent } from 'presentations/pages/result/result.component';

import { routes } from './app.routes';

describe('app routes', () => {
  it('should have expected routes', () => {
    expect(routes).toEqual([
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
    ]);
  });
});
