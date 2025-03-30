from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class PongResponse(BaseModel):
    message: str


class CreateActivityResponse(BaseModel):
    activity_id: UUID
    created_at: datetime
