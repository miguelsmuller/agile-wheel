import { Activity } from 'domain/model';

/**
 * DTO for the response returned after closing an activity.
 */
export interface CloseActivityResponse {
  activity: Activity;
}
