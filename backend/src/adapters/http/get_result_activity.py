import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.adapters.http.schemas import (
    ActivityForResultResponse,
    ResultResponse,
)
from src.application.ports.input.get_activity_result_port import GetActivityResultPort
from src.config.dependencies import get_result_activity_service
from src.domain.exceptions import ActivityNotFoundError

logger = logging.getLogger(__name__)
router = APIRouter()

__all__ = ["router"]


@router.get(
    "/activity/{activity_id}/result",
    summary="Retrieve activity result",
    status_code=status.HTTP_200_OK,
    response_model=ResultResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Activity result retrieved successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Activity not found with the provided identifier."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server responded with an unknown error."
        },
    },
)
async def get_result(
    activity_id: Annotated[UUID, Path(title="Activity identifier")],
    activity_service: GetActivityResultPort = Depends(get_result_activity_service),
):
    """Retrieve the result of a given activity by its unique identifier."""

    log_data = {"activity_id": activity_id}

    try:
        logger.debug("[GET_ACTIVITY_RESULT] Request Received", extra=log_data)

        activity = await activity_service.get_activity_result(activity_id)

    except ActivityNotFoundError as error:
        raise handle_not_found(error) from error

    except Exception as error:
        log_data["error"] = str(error)
        raise handle_unexpected_error(log_data, error) from error

    return ResultResponse(
        activity = ActivityForResultResponse.from_activity(activity.activity),
        result = activity.result
    )

def handle_not_found(error: ActivityNotFoundError) -> HTTPException:
    """Handle the case when an activity is not found."""

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(error)
    )

def handle_unexpected_error(log_data: dict, error: Exception) -> HTTPException:
    """Handle unexpected errors, logging them."""

    logger.exception("[GET_ACTIVITY_RESULT] Unexpected error", extra=log_data)

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Unexpected error occurred: {error}"
    )
