import { Routes } from '@angular/router';
import { ResultComponent } from './pages/result/result.component';
import { ActivityComponent } from './pages/activity/activity.component';
import { CreateActivityComponent } from './pages/create-activity/create-activity.component';
import { EnterActivityComponent } from './pages/enter-activity/enter-activity.component';

export const routes: Routes = [
    { path: '', redirectTo: 'create-activity', pathMatch: 'full' },
    { path: 'create-activity', component: CreateActivityComponent },
    { path: 'enter-activity', component: EnterActivityComponent },
    { path: 'activity/:id', component: ActivityComponent },
    { path: 'activity/:id/result', component: ResultComponent },
    { path: '**', redirectTo: 'create-activity' },
];
