import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status
from src.adapters.input.http.schemas import (
    ActivityResponse,
    JoinRequest,
    JoinResponse,
    ParticipantResponse,
)
from src.application.ports.input.join_activity_port import JoinActivityPort
from src.config.dependencies import get_join_activity_service
from src.domain.entities.participant import Participant

router = APIRouter()
router_params = {
    "status_code": status.HTTP_200_OK,
    "responses": {
        status.HTTP_200_OK: {"description": "Join activity successfully."},
    },
    "response_model": JoinResponse,
}


@router.patch("/activity/{activity_id}/join", **router_params)
async def post_activity_join(
    activity_id: Annotated[UUID, Path(title="The identifier of the actvity")],
    request: JoinRequest,
    join_activity_service: JoinActivityPort = Depends(get_join_activity_service),
):
    try:
        activity, participant = await join_activity_service.execute(
            activity_id=activity_id,
            participant=Participant(
                name=request.participant.name,
                email=request.participant.email,
                role="regular"
            )
        )

    except ReferenceError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity not found: {error}"
        ) from error

    except Exception as error:
        logging.error("[patch][/activity] %s", str(error))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {error}"
        ) from error

    return JoinResponse(
        participant=ParticipantResponse.from_participant(participant=participant),
        activity=ActivityResponse.from_activity(activity=activity)
    )
