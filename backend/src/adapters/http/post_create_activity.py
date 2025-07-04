import logging

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.ports.input.create_activity_port import CreateActivityPort
from src.config.dependencies import get_create_activity_service
from src.domain.entities.participant import Participant

from .schemas import (
    ActivityResponse,
    CreateActivityRequest,
    CreateActivityResponse,
    ParticipantResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/activity",
    summary="Create a new activity with the specified owner",
    status_code= status.HTTP_201_CREATED,
    response_model= CreateActivityResponse,
    responses= {
        status.HTTP_201_CREATED: {
            "description": "Activity created successfully."
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation error for the request data.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server responded with an unknown error."
        },
    },
)
async def post_activity(
    activity_request: CreateActivityRequest,
    create_activity_service: CreateActivityPort = Depends(get_create_activity_service),
):
    """Create a new activity with the provided owner participant information."""

    log_data = {"request": activity_request}

    owner = Participant(
        email=activity_request.owner.email,
        name=activity_request.owner.name,
        role="owner"
    )

    try:
        logger.debug("[POST_ACTIVITY_CREATE] Request Received", extra=log_data)

        activity = await create_activity_service.execute(owner=owner)

    except Exception as error:
        log_data["error"] = str(error)
        raise handle_unexpected_error(log_data, error) from error

    return CreateActivityResponse(
        participant=ParticipantResponse.from_participant(participant=owner),
        activity=ActivityResponse.from_activity(activity=activity)
    )

def handle_unexpected_error(log_data: dict, error: Exception) -> HTTPException:
    """Handle unexpected errors, logging them."""

    logger.exception("[POST_ACTIVITY_CREATE] Unexpected error", extra=log_data)

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Unexpected error occurred: {error}"
    )
