import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { SubmitEvaluationService } from './submit-evaluation.usecase';
import { CloseActivityService } from './close-activity.usecase';
import { Activity, DimensionWithScores, Participant } from '@models/activity.model';
import { clearDataFromLocalStorage } from '@utils/utils';

/**
 * Facade service to manage the activity flow, including submitting evaluations
 * and closing activities when necessary.
 */
@Injectable({ providedIn: 'root' })
export class ActivityFlowFacade {
  constructor(
    private readonly submitEvaluation: SubmitEvaluationService,
    private readonly closeActivity: CloseActivityService,
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
  async submitActivityFlow(
    activity: Activity,
    participant: Participant,
    evaluation: DimensionWithScores[]
  ): Promise<void> {
    this.submitEvaluation.submitEvaluation(activity, participant, evaluation);

    if (activity.owner.id === participant.id) {
      this.closeActivity.closeActivity(activity, participant);

      const redirectTo = `activity/${activity.activity_id}/result`;
      clearDataFromLocalStorage();
      this.router.navigate([redirectTo]);
    }
  }
}
