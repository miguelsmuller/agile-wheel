from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Path, status
from fastapi.responses import JSONResponse
from src.adapters.input.schemas import CloseResponse
from src.adapters.output.activity_repository_adapter import ActivityRepositoryAdapter
from src.application.ports.input.close_activity_port import CloseActivityPort
from src.application.usecase.close_activity_service import CloseActivityService

router = APIRouter()

repository = ActivityRepositoryAdapter()
service = CloseActivityService(repository=repository)


@router.post(
    "/activity/{activity_id}/close",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Close activity successfully."},
        status.HTTP_403_FORBIDDEN: {"description": "Permission denied."},
    },
    response_model=CloseResponse,
)
async def close_activity(
    activity_id: Annotated[str, Path(title="The identifier of the actvity")],
    participant_id: Annotated[
        str, Header(alias="X-Participant-Id", title="The identifier of the participant")
    ],
    close_activity_service: CloseActivityPort = Depends(lambda: service),
):
    try:
        closed_activity = await close_activity_service.execute(
            activity_id=UUID(activity_id),
            participant_id_requested=UUID(participant_id)
        )
    except PermissionError as e:
        return JSONResponse({"error": str(e)}, status.HTTP_403_FORBIDDEN)

    return CloseResponse(activity_id=closed_activity.id)
