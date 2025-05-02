from fastapi import APIRouter, Depends, status
from src.adapters.input.http.schemas import (
    ActivityResponse,
    CreateActivityRequest,
    CreateActivityResponse,
    ParticipantResponse,
)
from src.adapters.output.activity_repository_adapter import ActivityRepositoryAdapter
from src.application.ports.input.create_activity_port import CreateActivityPort
from src.application.usecase.create_activity_service import CreateActivityService
from src.domain.entities.participant import Participant

router = APIRouter()

repository = ActivityRepositoryAdapter()
service = CreateActivityService(repository=repository)


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
    create_activity_service: CreateActivityPort = Depends(lambda: service),
):
    owner = Participant(
        email=activity_request.owner.email,
        name=activity_request.owner.name,
        role="owner"
    )

    activity = await create_activity_service.execute(owner=owner)

    return CreateActivityResponse(
        participant=ParticipantResponse.from_participant(participant=owner),
        activity=ActivityResponse.from_activity(activity=activity)
    )
