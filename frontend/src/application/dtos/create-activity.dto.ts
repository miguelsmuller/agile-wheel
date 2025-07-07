import { Participant, Activity } from 'domain/model';

/**
 * DTOs for creating a new activity.
 */
export interface CreateActivityRequest {
  name: string;
  email: string;
}

/**
 * DTO for the response returned after creating a new activity.
 */
export interface CreateActivityResponse {
  participant: Participant;
  activity: Activity;
}
