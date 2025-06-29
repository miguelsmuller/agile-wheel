import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status
from src.adapters.input.http.schemas import (
    ActivityForResultResponse,
    ResultResponse,
)
from src.application.ports.input.get_activity_port import GetActivityPort
from src.config.dependencies import get_status_activity_service

logger = logging.getLogger(__name__)
logger_prefix = "[GET_ACTIVITY_RESULT]"

router = APIRouter()
router_params = {
    "status_code": status.HTTP_200_OK,
    "responses": {
        status.HTTP_200_OK: {"description": "Successfully retrieved the activity result."},
        status.HTTP_404_NOT_FOUND: {"description": "Activity not found."},
    },
    "response_model": ResultResponse,
}


@router.get("/activity/{activity_id}/result", **router_params)
async def get_result(
    activity_id: Annotated[UUID, Path(title="The identifier of the actvity")],
    activity_service: GetActivityPort = Depends(get_status_activity_service),
):
    try:
        logger.debug("%s Request", logger_prefix)
        activity_with_result = await activity_service.get_activity_with_result(activity_id)

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

    return ResultResponse(
        activity = ActivityForResultResponse.from_activity(activity=activity_with_result.activity),
        result = activity_with_result.result
    )
