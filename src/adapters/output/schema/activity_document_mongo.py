from beanie import Document
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from src.application.domain.models.activity import Activity, Participant, Dimension, ParticipantEvaluation
from src.application.domain.models.evaluation import Rating


class ParticipantModel(BaseModel):
    id: UUID
    name: str
    role: str
    email: str

class DimensionModel(BaseModel):
    id: str
    dimension: str
    comments: Optional[str] = None

class RatingModel(BaseModel):
    dimension_id: UUID
    score: float
    comments: Optional[str] = None

class ParticipantEvaluationModel(BaseModel):
    participant_id: UUID
    ratings: List[RatingModel]

class ActivityDocument(Document):
    app_id: UUID
    created_at: datetime
    participants: List[ParticipantModel]
    dimensions: List[DimensionModel]
    evaluations: List[ParticipantEvaluationModel]

    class Settings:
        name = "activities"

    @classmethod
    def from_domain(cls, activity: Activity) -> "ActivityDocument":
        return cls(
            app_id=activity.id,
            created_at=activity.created_at,
            participants=[ParticipantModel(**p.__dict__) for p in activity.participants],
            dimensions=[DimensionModel(**d.__dict__) for d in activity.dimensions],
            evaluations=[
                ParticipantEvaluationModel(
                    participant_id=e.participant_id,
                    ratings=[RatingModel(**r.__dict__) for r in e.ratings]
                ) for e in activity.evaluations
            ]
        )

    def to_domain(self) -> Activity:
        return Activity(
            id=self.app_id,
            created_at=self.created_at,
            participants=[Participant(**p.dict()) for p in self.participants],
            dimensions=[Dimension(**d.dict()) for d in self.dimensions],
            evaluations=[
                ParticipantEvaluation(
                    participant_id=e.participant_id,
                    ratings=[Rating(**r.dict()) for r in e.ratings]
                ) for e in self.evaluations
            ]
        )
