import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { DynamicComponent } from './pages/dynamic/dynamic.component';

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'home', component: HomeComponent },
    { path: 'dynamic', component: DynamicComponent },
];
