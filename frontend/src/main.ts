import { bootstrapApplication } from '@angular/platform-browser';
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';


import { CreateActivityUseCase } from '@use-cases/create-activity.usecase';
import { CREATE_ACTIVITY_USE_CASE_PORT } from 'application/ports/create-activity-use-case-port';

import { EnterActivityUseCase } from '@use-cases/enter-activity.usecase';
import { ENTER_ACTIVITY_USE_CASE_PORT } from 'application/ports/enter-activity-use-case-port';

import { SubmitEvaluationUseCase } from '@use-cases/submit-evaluation.usecase';
import { SUBMIT_EVALUATION_USE_CASE_PORT } from 'application/ports/submit-evaluation-use-case-port';

import { CloseActivityUserCase } from '@use-cases/close-activity.usecase';
import { CLOSE_ACTIVITY_USE_CASE_PORT } from 'application/ports/close-activity-use-case-port';

import { ActivityStreamUseCase } from '@use-cases/activity-stream.usecase';
import { ACTIVITY_STREAM_USE_CASE_PORT } from 'application/ports/activity-stream-use-case-port';

import { ActivityFlowFacade } from '@use-cases/activity-flow.facade';
import { ACTIVITY_FLOW_USE_CASE_PORT } from 'application/ports/activity-flow-use-case-port';

import { routes } from './application/routes/app.routes';

import { AppComponent } from './presentations/app.component';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(),
    { provide: CREATE_ACTIVITY_USE_CASE_PORT, useClass: CreateActivityUseCase },
    { provide: ENTER_ACTIVITY_USE_CASE_PORT, useClass: EnterActivityUseCase },
    { provide: SUBMIT_EVALUATION_USE_CASE_PORT, useClass: SubmitEvaluationUseCase },
    { provide: CLOSE_ACTIVITY_USE_CASE_PORT, useClass: CloseActivityUserCase },
    { provide: ACTIVITY_STREAM_USE_CASE_PORT, useClass: ActivityStreamUseCase },
    { provide: ACTIVITY_FLOW_USE_CASE_PORT, useClass: ActivityFlowFacade },
  ],
};

bootstrapApplication(AppComponent, appConfig).catch(err => console.error(err));
