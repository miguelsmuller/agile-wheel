from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Header, Path, status
from fastapi.responses import JSONResponse
from src.adapters.input.schemas import StatusResponse
from src.domain.entities.activity import Activity

router = APIRouter()


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
    activity_id: Annotated[str, Path(title="The identifier of the actvity")],
    participant_id: Annotated[
        str, Header(alias="X-Participant-Id", title="The identifier of the participant")
    ],
):
    activity_id = UUID(activity_id)

    try:
        activity = Activity()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    return StatusResponse(
        activity = activity
    )
