from fastapi import APIRouter, Depends, status

from src.adapters.input.schemas.schemas import JoinRequest, JoinResponse

from src.application.domain.models.participant import Participant
from src.application.domain.models.activity import Activity
from src.application.ports.input.join_activity_port import JoinActivityPort
from src.application.usecase.join_activity_service import JoinActivityService

from fastapi import APIRouter, status


router = APIRouter()


@router.patch(
    "/activity/join",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Join activity successfully."},
    },
    response_model=JoinResponse,
)
def join_activity(
    request: JoinRequest,
    join_activity_service: JoinActivityPort = Depends(JoinActivityService.get_service)
):
    # Search for the activity
    activity = Activity()
    activity.id = request.activity_id

    # Create the participant
    participant = Participant(
        name=request.participant_name, 
        email=request.participant_email
    )

    # Join the participant to the activity
    join_activity_service.execute(activity=activity, participant=participant)

    # Return the activity
    return JoinResponse(
        activity_id=activity.id, 
        participant_id=participant.id
    )
