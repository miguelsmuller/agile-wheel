import { Participant, Activity } from 'domain/model';

/**
 * DTOs for entering an existing activity.
 */
export interface EnterActivityRequest {
  name: string;
  email: string;
}

/**
 * DTO for the response returned after entering an activity.
 */
export interface EnterActivityResponse {
  participant: Participant;
  activity: Activity;
}
