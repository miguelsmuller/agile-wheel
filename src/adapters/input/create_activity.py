from fastapi import APIRouter, Depends, status

from src.adapters.input.schemas.schemas import CreateActivityRequest, CreateActivityResponse

from src.application.domain.models.participant import Participant
from src.application.ports.input.create_activity_port import CreateActivityPort
from src.application.usecase.create_activity_service import CreateActivityService

from fastapi import APIRouter, status


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
