import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Path, status

from src.adapters.http.schemas import ActivityResponse, StatusResponse
from src.application.ports.input.get_activity_status_port import GetActivityStatusPort
from src.config.dependencies import get_status_activity_service

logger = logging.getLogger(__name__)
router = APIRouter()

__all__ = ["router"]


@router.get(
    "/activity/{activity_id}",
    summary="Retrieve the status of an activity by its identifier",
    status_code=status.HTTP_200_OK,
    response_model= StatusResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "Activity status retrieved successfully."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Activity not found with the provided identifier."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server responded with an unknown error."
        },
    },
)
async def get_status(
    activity_id: Annotated[UUID, Path(title="Activity identifier")],
    participant_id: Annotated[
        UUID, Header(alias="X-Participant-Id", title="Participant identifier")
    ],
    status_activity_service: GetActivityStatusPort = Depends(get_status_activity_service),
):
    """Retrieve the status of a given activity by its unique identifier."""

    log_data = {"activity_id": activity_id, "participant_id": participant_id}

    try:
        logger.debug("[GET_ACTIVITY_STATUS] Request Received", extra=log_data)

        activity = await status_activity_service.get_activity_status(activity_id , participant_id)

    except ReferenceError as error:
        raise handle_not_found(error) from error

    except Exception as error:
        log_data["error"] = str(error)
        raise handle_unexpected_error(log_data, error) from error

    return StatusResponse(
        activity = ActivityResponse.from_activity(activity=activity)
    )

def handle_not_found(error: ReferenceError) -> HTTPException:
    """Handle the case when an activity is not found."""

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(error)
    )

def handle_unexpected_error(log_data: dict, error: Exception) -> HTTPException:
    """Handle unexpected errors, logging them."""

    logger.exception("[GET_ACTIVITY_STATUS] Unexpected error", extra=log_data)

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Unexpected error occurred: {error}"
    )
