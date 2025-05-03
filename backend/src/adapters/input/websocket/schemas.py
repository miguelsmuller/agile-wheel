from datetime import datetime

from pydantic import BaseModel
from src.domain.entities.activity import Activity
from src.domain.entities.participant import Participant


class ParticipantResponse(BaseModel):
    id: str
    name: str
    email: str

    @classmethod
    def from_participant(cls, participant: Participant) -> "ParticipantResponse":
        return cls(
            id=str(participant.id),
            name=participant.name,
            email=participant.email
        )

class ActivityStream(BaseModel):
    activity_id: str
    created_at: datetime
    is_opened: bool
    participants: list[ParticipantResponse]

    @classmethod
    def from_activity(cls, activity: Activity) -> "ActivityStream":
        return cls(
            activity_id=str(activity.id),
            created_at=activity.created_at,
            is_opened=activity.is_opened,
            participants=[
                ParticipantResponse.from_participant(participant)
                for participant in activity.participants
            ]
        )
