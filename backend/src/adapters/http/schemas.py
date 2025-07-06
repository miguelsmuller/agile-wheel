from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from src.domain.aggregations.activity_result import ActivityResult
from src.domain.entities.activity import Activity
from src.domain.entities.dimension import Dimension, Principle
from src.domain.entities.participant import Participant

# ================================================================
# Participant Schemas
# ================================================================

class ParticipantResponse(BaseModel):
    id: str
    name: str
    email: EmailStr

    @classmethod
    def from_participant(cls, participant: Participant) -> "ParticipantResponse":
        return cls(
            id=str(participant.id),
            name=participant.name,
            email=participant.email
        )

class ParticipantRequest(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr

# ================================================================
# Principle and Dimension Schemas
# ================================================================

class PrincipleResponse(BaseModel):
    id: str
    name: str
    comments: str | None = None

    @classmethod
    def from_principle(cls, principle: Principle) -> "PrincipleResponse":
        return cls(
            id=principle.id,
            name=principle.name,
            comments=principle.comments
        )

class DimensionResponse(BaseModel):
    id: str
    name: str
    comments: str | None = None
    principles: list[PrincipleResponse]

    @classmethod
    def from_dimension(cls, dimension: Dimension) -> "DimensionResponse":
        return cls(
            id=dimension.id,
            name=dimension.name,
            comments=dimension.comments,
            principles=[
                PrincipleResponse.from_principle(principle)
                for principle in dimension.principles
            ]
        )

class RatingRequest(BaseModel):
    principle_id: str
    score: float
    comments: str | None = None

# ================================================================
# Activity Schemas
# ================================================================

class ActivityResponse(BaseModel):
    activity_id: str
    created_at: datetime
    is_opened: bool
    owner: ParticipantResponse
    participants: list[ParticipantResponse]
    dimensions: list[DimensionResponse]

    @classmethod
    def from_activity(cls, activity: Activity) -> "ActivityResponse":
        owner = next((p for p in activity.participants if p.role == "owner"), None)

        return cls(
            activity_id=str(activity.id),
            created_at=activity.created_at,
            is_opened=activity.is_opened,
            owner=ParticipantResponse.from_participant(owner),
            participants=[
                ParticipantResponse.from_participant(participant)
                for participant in activity.participants
            ],
            dimensions=[
                DimensionResponse.from_dimension(dimension)
                for dimension in activity.dimensions
            ]
        )

# Alternative views

class ActivityForResultResponse(ActivityResponse):
    owner: ParticipantResponse | None = Field(exclude=True)
    participants: list[ParticipantResponse] | None = Field(exclude=True)
    dimensions: list[DimensionResponse] | None = Field(exclude=True)

# ================================================================
# Request and Response Schemas for requests and responses
# ================================================================

class CreateActivityRequest(BaseModel):
    owner: ParticipantRequest

class CreateActivityResponse(BaseModel):
    participant: ParticipantResponse
    activity: ActivityResponse

# ========================

class JoinRequest(BaseModel):
    participant: ParticipantRequest

class JoinResponse(BaseModel):
    participant: ParticipantResponse
    activity: ActivityResponse

# ========================

class EvaluationRequest(BaseModel):
    ratings: list[RatingRequest]

class EvaluationResponse(BaseModel):
    activity_id: str
    evaluation_id: str

# ========================

class StatusResponse(BaseModel):
    activity: ActivityResponse

# ========================

class CloseResponse(BaseModel):
    activity: ActivityResponse

# ========================

class ResultResponse(BaseModel):
    activity: ActivityForResultResponse
    result: ActivityResult
