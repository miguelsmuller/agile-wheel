import logging

from fastapi import APIRouter, Depends, HTTPException, status
from src.adapters.input.http.schemas import (
    ActivityResponse,
    CreateActivityRequest,
    CreateActivityResponse,
    ParticipantResponse,
)
from src.application.ports.input.create_activity_port import CreateActivityPort
from src.config.dependencies import get_create_activity_service
from src.domain.entities.participant import Participant

router = APIRouter()

@router.post(
    "/activity",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Activity created successfully."},
    },
    response_model=CreateActivityResponse,
)
async def activity(
    activity_request: CreateActivityRequest,
    create_activity_service: CreateActivityPort = Depends(get_create_activity_service),
):
    owner = Participant(
        email=activity_request.owner.email,
        name=activity_request.owner.name,
        role="owner"
    )

    try:
        activity = await create_activity_service.execute(owner=owner)

    except Exception as error:
        logging.error("[post][/activity] %s", str(error))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {error}"
        ) from error

    return CreateActivityResponse(
        participant=ParticipantResponse.from_participant(participant=owner),
        activity=ActivityResponse.from_activity(activity=activity)
    )
