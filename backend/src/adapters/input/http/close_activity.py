import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Path, status
from fastapi.responses import JSONResponse
from src.adapters.input.http.schemas import ActivityResponse, CloseResponse
from src.application.ports.input.close_activity_port import CloseActivityPort
from src.config.dependencies import get_close_activity_service

logger = logging.getLogger(__name__)
logger_prefix = "[post][/activity/$/close]"

router = APIRouter()
router_params = {
    "status_code": status.HTTP_200_OK,
    "responses": {
        status.HTTP_200_OK: {"description": "Close activity successfully."},
        status.HTTP_403_FORBIDDEN: {"description": "Permission denied."},
    },
    "response_model": CloseResponse,
}


@router.post("/activity/{activity_id}/close", **router_params)
async def post_activity_close(
    activity_id: Annotated[UUID, Path(title="The identifier of the actvity")],
    participant_id: Annotated[
        UUID, Header(alias="X-Participant-Id", title="The identifier of the participant")
    ],
    close_activity_service: CloseActivityPort = Depends(get_close_activity_service),
):
    try:
        logger.debug("%s Request", logger_prefix)
        closed_activity = await close_activity_service.execute(
            activity_id=activity_id,
            participant_id_requested=participant_id
        )

    except PermissionError as e:
        return JSONResponse({"error": str(e)}, status.HTTP_403_FORBIDDEN)

    return CloseResponse(
        activity=ActivityResponse.from_activity(activity=closed_activity)
    )
