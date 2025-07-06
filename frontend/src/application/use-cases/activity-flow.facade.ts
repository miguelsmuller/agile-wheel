import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { clearDataFromLocalStorage } from '@adapters/local-storage/utils';
import { Activity, DimensionWithScores, Participant } from 'domain/model';
import { ActivityFlowUseCasePort } from 'application/ports/activity-flow-use-case-port';

import { SubmitEvaluationUseCase } from './submit-evaluation.usecase';
import { CloseActivityUserCase } from './close-activity.usecase';

/**
 * Facade service to manage the activity flow, including submitting evaluations
 * and closing activities when necessary.
 */
@Injectable({ providedIn: 'root' })
export class ActivityFlowFacade implements ActivityFlowUseCasePort {
  constructor(
    private readonly submitEvaluation: SubmitEvaluationUseCase,
    private readonly closeActivity: CloseActivityUserCase,
    private readonly router: Router
  ) {}

  /**
   * Submits an evaluation for an activity and closes the activity if the participant
   * is the owner of the activity.
   *
   * @param activity - The activity being evaluated.
   * @param participant - The participant submitting the evaluation.
   * @param evaluation - The evaluation data containing dimensions and scores.
   * @returns A promise that resolves when the flow is complete.
   */
  async execute(
    activity: Activity,
    participant: Participant,
    evaluation: DimensionWithScores[]
  ): Promise<void> {
    this.submitEvaluation.execute(activity, participant, evaluation);

    if (activity.owner.id === participant.id) {
      this.closeActivity.execute(activity, participant);

      const redirectTo = `activity/${activity.activity_id}/result`;
      clearDataFromLocalStorage();
      this.router.navigate([redirectTo]);
    }
  }
}
