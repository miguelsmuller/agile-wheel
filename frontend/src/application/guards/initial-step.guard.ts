import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

import { getActivityFromLocalStorage } from 'adapters/local-storage/utils';

@Injectable({ providedIn: 'root' })
export class InitialStepGuard implements CanActivate {
  constructor(private readonly router: Router) {}

  canActivate(): boolean {
    const activity = getActivityFromLocalStorage();

    if (activity) {
      console.error('[InitialStepGuard] Something went wrong.');
      this.router.navigate(['/activity', activity.activity_id]);
      return false;
    }

    return true;
  }
}
