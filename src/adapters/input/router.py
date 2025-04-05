from fastapi import APIRouter, Depends, status

from src.adapters.input.schemas.schemas import CreateActivityRequest, CreateActivityResponse, JoinRequest, JoinResponse, PongResponse

from src.application.domain.models.participant import Participant
from src.application.domain.models.activity import Activity
from src.application.ports.input.create_activity_port import CreateActivityPort
from src.application.ports.input.join_activity_port import JoinActivityPort
from src.application.usecase.create_activity_service import CreateActivityService
from src.application.usecase.join_activity_service import JoinActivityService

from fastapi import APIRouter, status


router = APIRouter()


@router.get("/")
def root():
    return {"Hello": "World"}


@router.get(
    "/ping",
    responses={
        status.HTTP_200_OK: {"description": "Return a pong message"},
    },
    response_model=PongResponse,
)
async def ping():
    return PongResponse(message="pong")


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
    create_activity_service: CreateActivityPort = Depends(CreateActivityService.get_service)
):
    activity = await create_activity_service.execute(
        owner = Participant(
            email=activity_request.owner_email, 
            name=activity_request.owner_name,
            role="owner"
        )
    )
    
    return CreateActivityResponse(
        activity_id=activity.id, 
        created_at=activity.created_at,
        dimensions=activity.dimensions
    )


@router.patch(
    "/activity/join",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Join activity successfully."},
    },
    response_model=JoinResponse,
)
def join(
    request: JoinRequest,
    join_activity_service: JoinActivityPort = Depends(JoinActivityService.get_service)
):
    # Search for the activity
    activity = Activity()
    activity.id = request.activity_id

    # Create the participant
    participant = Participant(
        name=request.participant_name, 
        role=request.participant_role
    )

    # Join the participant to the activity
    join_activity_service.execute(activity=activity, participant=participant)

    # Return the activity
    return JoinResponse(
        activity_id=activity.id, 
        participant_id=participant.id
    )
