export interface Participant {
  id: string;
  name: string;
}

export interface Principle {
  id: string;
  principle: string;
  comments?: string;
}

export interface Dimension {
  id: string;
  dimension: string;
  comments?: string;
  principles: Principle[];
}

export interface Activity {
  activity_id: string;
  created_at: string;
  is_opened: boolean;
  owner_name: string;
  participants: Participant[];
  dimensions: Dimension[];
}