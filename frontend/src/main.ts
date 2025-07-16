import { provideHttpClient } from '@angular/common/http';
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';

import { echartsProvider } from 'adapters/echarts/echarts.token';
import { ACTIVITY_FLOW_USE_CASE_PORT } from 'application/ports/activity-flow-use-case-port';
import { ACTIVITY_STREAM_USE_CASE_PORT } from 'application/ports/activity-stream-use-case-port';
import { CLOSE_ACTIVITY_USE_CASE_PORT } from 'application/ports/close-activity-use-case-port';
import { CREATE_ACTIVITY_USE_CASE_PORT } from 'application/ports/create-activity-use-case-port';
import { ENTER_ACTIVITY_USE_CASE_PORT } from 'application/ports/enter-activity-use-case-port';
import { GET_ACTIVITY_RESULT_USE_CASE_PORT } from 'application/ports/get-activity-result-use-case-port';
import { SUBMIT_EVALUATION_USE_CASE_PORT } from 'application/ports/submit-evaluation-use-case-port';
import { routes } from 'application/routes/app.routes';
import { ActivityFlowFacade } from 'application/use-cases/activity-flow.facade';
import { ActivityStreamUseCase } from 'application/use-cases/activity-stream.usecase';
import { CloseActivityUserCase } from 'application/use-cases/close-activity.usecase';
import { CreateActivityUseCase } from 'application/use-cases/create-activity.usecase';
import { EnterActivityUseCase } from 'application/use-cases/enter-activity.usecase';
import { GetActivityResultUseCase } from 'application/use-cases/get-activity-result.usecase';
import { SubmitEvaluationUseCase } from 'application/use-cases/submit-evaluation.usecase';
import { AppComponent } from 'presentations/app.component';

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
    { provide: GET_ACTIVITY_RESULT_USE_CASE_PORT, useClass: GetActivityResultUseCase },
    echartsProvider,
  ],
};

bootstrapApplication(AppComponent, appConfig).catch(err => console.error(err));
