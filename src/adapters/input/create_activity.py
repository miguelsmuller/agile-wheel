from fastapi import APIRouter, Depends, status
from src.adapters.input.schemas import (
    CreateActivityRequest,
    CreateActivityResponse,
    DimensionResponse,
    PrincipleResponse,
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
    activity = await create_activity_service.execute(
        owner=Participant(
            email=activity_request.owner_email, name=activity_request.owner_name, role="owner"
        )
    )

    dimensions_response = [
        DimensionResponse(
            id=dimension.id,
            dimension=dimension.dimension,
            comments=dimension.comments,
            principles=[
                PrincipleResponse(
                    id=principle.id,
                    principle=principle.principle,
                    comments=principle.comments,
                )
                for principle in dimension.principles
            ],
        )
        for dimension in activity.dimensions
    ]

    return CreateActivityResponse(
        activity_id=activity.id,
        created_at=activity.created_at,
        dimensions=dimensions_response
    )
