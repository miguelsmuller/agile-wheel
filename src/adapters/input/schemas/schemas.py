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
