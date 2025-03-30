from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import List

from src.application.domain.models.dimension import Dimension


class PongResponse(BaseModel):
    message: str


class CreateActivityResponse(BaseModel):
    activity_id: UUID
    created_at: datetime
    dimensions: List[Dimension]


class JoinRequest(BaseModel):
    activity_id: UUID
    participant_name: str
    participant_role: str

class JoinResponse(BaseModel):
    activity_id: UUID
    participant_id: UUID
