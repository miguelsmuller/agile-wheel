from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status
from src.adapters.input.schemas import JoinRequest, JoinResponse
from src.adapters.output.activity_repository_adapter import ActivityRepositoryAdapter
from src.application.ports.input.join_activity_port import JoinActivityPort
from src.application.usecase.join_activity_service import JoinActivityService
from src.domain.entities.participant import Participant

router = APIRouter()

repository = ActivityRepositoryAdapter()
service = JoinActivityService(repository=repository)

@router.patch(
    "/activity/{activity_id}/join",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Join activity successfully."},
    },
    response_model=JoinResponse,
)
async def join_activity(
    activity_id: Annotated[str, Path(title="The identifier of the actvity")],
    request: JoinRequest,
    join_activity_service: JoinActivityPort = Depends(lambda: service),
):
    activity, participant = await join_activity_service.execute(
        activity_id=UUID(activity_id),
        participant=Participant(
            name=request.participant_name,
            email=request.participant_email,
            role="regular"
        )
    )

    return JoinResponse(
        activity_id=activity.id,
        participant_id=participant.id
    )
