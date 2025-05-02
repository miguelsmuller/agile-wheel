from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse
from src.adapters.input.http.schemas import (
    ActivityResponse,
    JoinRequest,
    JoinResponse,
    ParticipantResponse,
)
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
    activity_id: Annotated[UUID, Path(title="The identifier of the actvity")],
    request: JoinRequest,
    join_activity_service: JoinActivityPort = Depends(lambda: service),
):
    try:

        activity, participant = await join_activity_service.execute(
            activity_id=activity_id,
            participant=Participant(
                name=request.participant.name,
                email=request.participant.email,
                role="regular"
            )
        )
    except ReferenceError as e:
        return JSONResponse({"error": str(e)}, status.HTTP_404_NOT_FOUND)

    return JoinResponse(
        participant=ParticipantResponse.from_participant(participant=participant),
        activity=ActivityResponse.from_activity(activity=activity)
    )
