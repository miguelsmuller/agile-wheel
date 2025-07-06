import { Participant } from 'domain/model';

/**
 * DTO for messages received from the activity stream.
 */
export interface ActivityStreamMessage {
  activity_id: string;
  created_at: string;
  is_opened: boolean;
  participants: Participant[];
}
