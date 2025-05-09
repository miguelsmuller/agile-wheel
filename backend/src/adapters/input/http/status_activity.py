from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Path, status
from src.adapters.input.http.schemas import ActivityResponse, StatusResponse
from src.adapters.output.activity_repository_adapter import ActivityRepositoryAdapter
from src.application.ports.input.status_activity_port import StatusActivityPort
from src.application.usecase.status_activity_service import StatusActivityService

router = APIRouter()

repository = ActivityRepositoryAdapter()
service = StatusActivityService(repository=repository)

@router.get(
    "/activity/{activity_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Close activity successfully."},
        status.HTTP_404_NOT_FOUND: {"description": "Activity not found."},
    },
    response_model=StatusResponse,
)
async def status_activity(
    activity_id: Annotated[UUID, Path(title="The identifier of the actvity")],
    participant_id: Annotated[
        UUID, Header(alias="X-Participant-Id", title="The identifier of the participant")
    ],
    status_activity_service: StatusActivityPort = Depends(lambda: service),
):
    activity = await status_activity_service.execute(activity_id , participant_id)

    return StatusResponse(
        activity = ActivityResponse.from_activity(activity=activity)
    )
