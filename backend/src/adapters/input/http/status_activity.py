import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Path, status
from src.adapters.input.http.schemas import ActivityResponse, StatusResponse
from src.application.ports.input.status_activity_port import StatusActivityPort
from src.config.dependencies import get_status_activity_service

logger = logging.getLogger(__name__)

router = APIRouter()
router_params = {
    "status_code": status.HTTP_200_OK,
    "responses": {
        status.HTTP_200_OK: {"description": "Close activity successfully."},
        status.HTTP_404_NOT_FOUND: {"description": "Activity not found."},
    },
    "response_model": StatusResponse,
}

@router.get("/activity/{activity_id}", **router_params)
async def status_activity(
    activity_id: Annotated[UUID, Path(title="The identifier of the actvity")],
    participant_id: Annotated[
        UUID, Header(alias="X-Participant-Id", title="The identifier of the participant")
    ],
    status_activity_service: StatusActivityPort = Depends(get_status_activity_service),
):
    try:
        activity = await status_activity_service.execute(activity_id , participant_id)

    except ReferenceError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity not found: {error}"
        ) from error

    except Exception as error:
        logger.error("[get][/activity] %s", str(error))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {error}"
        ) from error

    return StatusResponse(
        activity = ActivityResponse.from_activity(activity=activity)
    )
