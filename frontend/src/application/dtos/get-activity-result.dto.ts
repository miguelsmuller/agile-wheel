import { ActivityResult } from 'domain/model';

export interface ActivityForResult {
  activity_id: string;
  created_at: string;
  is_opened: boolean;
}

export interface GetActivityResultResponse {
  activity: ActivityForResult;
  result: ActivityResult;
}
