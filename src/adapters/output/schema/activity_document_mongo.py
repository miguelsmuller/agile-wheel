from datetime import datetime
from uuid import UUID

from beanie import Document
from pydantic import BaseModel

from src.domain.entities.activity import (
    Activity,
    Dimension,
    Participant,
    ParticipantEvaluation,
)
from src.domain.entities.evaluation import Rating


class ParticipantModel(BaseModel):
    id: str
    name: str
    role: str
    email: str

class DimensionModel(BaseModel):
    id: str
    dimension: str
    comments: str | None = None

class RatingModel(BaseModel):
    dimension_id: str
    score: float
    comments: str | None = None

class ParticipantEvaluationModel(BaseModel):
    participant_id: str
    ratings: list[RatingModel]

class ActivityDocument(Document):
    app_id: str
    opened: bool = False
    created_at: datetime
    participants: list[ParticipantModel]
    dimensions: list[DimensionModel]
    evaluations: list[ParticipantEvaluationModel]

    class Settings:
        name = "activities"

    @classmethod
    def from_domain(cls, activity: Activity) -> "ActivityDocument":
        return cls(
            app_id=str(activity.id),
            created_at=activity.created_at,
            opened=activity.opened,
            participants=[
                ParticipantModel(
                    id=str(p.id),
                    name=p.name,
                    role=p.role,
                    email=p.email
                ) for p in activity.participants],
            dimensions=[
                DimensionModel(
                    id=str(d.id),
                    dimension=d.dimension,
                    comments=d.comments
                ) for d in activity.dimensions
            ],
            evaluations=[
                ParticipantEvaluationModel(
                    participant_id=e.participant_id,
                    ratings=[
                        RatingModel(
                            dimension_id=str(r.dimension_id),
                            score=r.score,
                            comments=r.comments
                        ) for r in e.ratings
                    ]
                ) for e in activity.evaluations
            ]
        )

    def to_domain(self) -> Activity:
        return Activity(
            id=UUID(self.app_id),
            created_at=self.created_at,
            opened=self.opened,
            participants=[
                Participant(
                    id=UUID(p.id),
                    name=p.name,
                    role=p.role,
                    email=p.email
                ) for p in self.participants
            ],
            dimensions=[
                Dimension(
                    id=d.id,
                    dimension=d.dimension,
                    comments=d.comments
                ) for d in self.dimensions
            ],
            evaluations=[
                ParticipantEvaluation(
                    participant_id=e.participant_id,
                    ratings=[
                        Rating(
                            dimension_id=UUID(r.dimension_id),
                            score=r.score,
                            comments=r.comments
                        ) for r in e.ratings
                    ]
                ) for e in self.evaluations
            ]
        )
