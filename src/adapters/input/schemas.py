from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator

from src.domain.entities.dimension import Dimension


class PongResponse(BaseModel):
    message: str

class CreateActivityRequest(BaseModel):
    owner_name: str
    owner_email: EmailStr

    @field_validator("owner_name")
    @classmethod
    def validator_name(cls, value):
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return value

class CreateActivityResponse(BaseModel):
    activity_id: UUID
    created_at: datetime
    dimensions: list[Dimension]


class JoinRequest(BaseModel):
    participant_name: str
    participant_email: EmailStr

    @field_validator("participant_name")
    @classmethod
    def validator_name(cls, value):
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return value

class JoinResponse(BaseModel):
    activity_id: UUID
    participant_id: UUID

class CloseResponse(BaseModel):
    activity_id: UUID
