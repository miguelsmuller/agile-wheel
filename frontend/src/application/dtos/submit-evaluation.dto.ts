import { Participant, Activity } from 'domain/model';

/**
 * DTO for each rating entry in a submit evaluation request.
 */
export interface SubmitEvaluationRatingRequest {
  principle_id: string;
  score: number;
  comments: string;
}

/**
 * DTO for the request to submit an evaluation for an activity.
 */
export interface SubmitEvaluationRequest {
  ratings: SubmitEvaluationRatingRequest[];
}

/**
 * DTO for the response returned after submitting an evaluation.
 */
export interface SubmitEvaluationResponse {
  participant: Participant;
  activity: Activity;
}
