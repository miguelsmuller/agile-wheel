import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Path, status
from fastapi.responses import JSONResponse

from src.adapters.http.schemas import ActivityResponse, CloseResponse
from src.application.ports.input.close_activity_port import CloseActivityPort
from src.config.dependencies import get_close_activity_service
from src.domain.exceptions import ActivityNotFoundError, PermissionDeniedError

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/activity/{activity_id}/close",
    summary="Close an activity by its identifier",
    status_code= status.HTTP_200_OK,
    response_model= CloseResponse,
    responses= {
        status.HTTP_200_OK: {
            "description": "Activity closed successfully."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Participant is not allowed to close this activity."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Activity not found with the provided identifier."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server responded with an unknown error."
        },
    },
)
async def post_activity_close(
    activity_id: Annotated[UUID, Path(title="The identifier of the actvity")],
    participant_id: Annotated[
        UUID, Header(alias="X-Participant-Id", title="The identifier of the participant")
    ],
    close_activity_service: CloseActivityPort = Depends(get_close_activity_service),
):
    """Close an activity by providing its identifier and the requesting participant ID."""

    log_data = {"activity_id": activity_id, "participant_id": participant_id}

    try:
        logger.debug("[POST_ACTIVITY_CLOSE] Request Received", extra=log_data)

        closed_activity = await close_activity_service.execute(
            activity_id=activity_id,
            participant_id_requested=participant_id
        )

    except PermissionDeniedError as error:
        raise handle_forbidden(error) from error

    except ActivityNotFoundError as error:
        raise handle_not_found(error) from error

    except Exception as error:
        log_data["error"] = str(error)
        raise handle_unexpected_error(log_data, error) from error

    return CloseResponse(
        activity=ActivityResponse.from_activity(activity=closed_activity)
    )

def handle_forbidden(error: PermissionError) -> JSONResponse:
    """Handle the case when the participant is not allowed to close the activity."""

    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Participant is not allowed to close this activity: {error}"
    )

def handle_not_found(error: ReferenceError) -> HTTPException:
    """Handle the case when an activity is not found."""

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Activity not found: {error}"
    )

def handle_unexpected_error(log_data: dict, error: Exception) -> HTTPException:
    """Handle unexpected errors, logging them."""

    logger.exception("[POST_ACTIVITY_CLOSE] Unexpected error", extra=log_data)

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Unexpected error occurred: {error}"
    )
