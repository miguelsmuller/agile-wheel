from datetime import datetime
from uuid import UUID

from beanie import Document
from pydantic import BaseModel
from src.domain.entities.activity import (
    Activity,
    Dimension,
    Participant,
)
from src.domain.entities.dimension import Principle
from src.domain.entities.evaluation import ParticipantEvaluation, Rating


class ParticipantModel(BaseModel):
    id: str
    name: str
    role: str
    email: str

class PrincipleModel(BaseModel):
    id: str
    principle: str
    comments: str | None = None

class DimensionModel(BaseModel):
    id: str
    dimension: str
    comments: str | None = None
    principles: list[PrincipleModel]

class RatingModel(BaseModel):
    principle_id: str
    score: float
    comments: str | None = None

class ParticipantEvaluationModel(BaseModel):
    id: str
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
        participants = [
            ParticipantModel(
                id=str(p.id),
                name=p.name,
                role=p.role,
                email=p.email
            ) for p in activity.participants
        ]
        dimensions = [
            DimensionModel(
                id=str(d.id),
                dimension=d.dimension,
                comments=d.comments,
                principles=[
                    PrincipleModel(
                        id=p.id,
                        principle=p.principle,
                        comments=p.comments
                    ) for p in d.principles
                ]
            ) for d in activity.dimensions
        ]
        evaluations = [
            ParticipantEvaluationModel(
                id=str(e.id),
                participant_id=str(e.participant_id),
                ratings=[
                    RatingModel(
                        principle_id=r.principle_id,
                        score=r.score,
                        comments=r.comments
                    ) for r in e.ratings
                ]
            ) for e in activity.evaluations
        ]

        return cls(
            app_id=str(activity.id),
            created_at=activity.created_at,
            opened=activity.opened,
            participants=participants,
            dimensions=dimensions,
            evaluations=evaluations
        )

    def to_domain(self) -> Activity:
        participants = [
            Participant(
                id=UUID(p.id),
                name=p.name,
                role=p.role,
                email=p.email
            ) for p in self.participants
        ]
        dimensions = [
            Dimension(
                id=d.id,
                dimension=d.dimension,
                comments=d.comments,
                principles=[
                    Principle(
                        id=p.id,
                        principle=p.principle,
                        comments=p.comments
                    ) for p in d.principles
                ]
            ) for d in self.dimensions
        ]

        evaluations = [
            ParticipantEvaluation(
                id=UUID(e.id),
                participant_id=UUID(e.participant_id),
                ratings=[
                    Rating(
                        principle_id=r.principle_id,
                        score=r.score,
                        comments=r.comments
                    ) for r in e.ratings
                ]
            ) for e in self.evaluations
        ]

        return Activity(
            id=UUID(self.app_id),
            created_at=self.created_at,
            opened=self.opened,
            participants=participants,
            dimensions=dimensions,
            evaluations=evaluations
        )
