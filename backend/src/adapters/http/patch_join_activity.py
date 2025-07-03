import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.adapters.http.schemas import (
    ActivityResponse,
    JoinRequest,
    JoinResponse,
    ParticipantResponse,
)
from src.application.ports.input.join_activity_port import JoinActivityPort
from src.config.dependencies import get_join_activity_service
from src.domain.entities.participant import Participant

logger = logging.getLogger(__name__)
router = APIRouter()


@router.patch(
    "/activity/{activity_id}/join",
    summary="Join an existing activity with participant information",
    status_code= status.HTTP_200_OK,
    response_model= JoinResponse,
    responses= {
        status.HTTP_200_OK: {
            "description": "Successfully joined the activity."
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Activity not found with the provided identifier."
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the request data.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server responded with an unknown error."
        },
    },
)
async def patch_join_activity(
    activity_id: Annotated[UUID, Path(title="The identifier of the actvity")],
    request: JoinRequest,
    join_activity_service: JoinActivityPort = Depends(get_join_activity_service),
):
    """Join an existing activity by providing participant information."""

    log_data = {"activity_id": activity_id, "request": request}

    try:
        logger.debug("[PATCH_ACTIVITY_JOIN] Request Received", extra=log_data)

        activity, participant = await join_activity_service.execute(
            activity_id=activity_id,
            participant=Participant(
                name=request.participant.name,
                email=request.participant.email,
                role="regular"
            )
        )

    except ReferenceError as error:
        raise handle_not_found(error) from error

    except Exception as error:
        log_data["error"] = str(error)
        raise handle_unexpected_error(log_data, error) from error

    return JoinResponse(
        participant=ParticipantResponse.from_participant(participant=participant),
        activity=ActivityResponse.from_activity(activity=activity)
    )

def handle_not_found(error: ReferenceError) -> HTTPException:
    """Handle the case when an activity is not found."""

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Activity not found: {error}"
    )

def handle_unexpected_error(log_data: dict, error: Exception) -> HTTPException:
    """Handle unexpected errors, logging them."""

    logger.exception("[PATCH_ACTIVITY_JOIN] Unexpected error", extra=log_data)

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Unexpected error occurred: {error}"
    )
