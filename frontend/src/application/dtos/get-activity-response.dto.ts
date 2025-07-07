import { Activity } from 'domain/model';

/**
 * DTO for the response returned when fetching an activity.
 */
export interface GetActivityResponse {
  activity: Activity;
}
