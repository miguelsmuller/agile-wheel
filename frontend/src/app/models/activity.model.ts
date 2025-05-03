export interface Participant {
  id: string;
  name: string;
  email: string;
}

export interface Principle {
  id: string;
  name: string;
  comments?: string;
}

export interface PrincipleWithScore extends Principle {
  score?: number;
}

export interface Dimension {
  id: string;
  name: string;
  comments?: string;
  principles: Principle[];
}

export interface DimensionWithScores extends Omit<Dimension, 'principles'> {
  principles: PrincipleWithScore[];
}

export interface Rating {
  id: string;
  score: number;
  comments?: string | null;
}

export interface ParticipantEvaluation {
  participantId: string;
  id: string;
  ratings: Rating[];
}

export interface Activity {
  activity_id: string;
  created_at: string;
  is_opened: boolean;
  owner: Participant;
  participants: Participant[];
  dimensions: Dimension[];
  evaluations: ParticipantEvaluation[]
}