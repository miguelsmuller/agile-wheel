from fastapi import APIRouter, status

from src.adapters.input.schemas.schemas import CreateActivityResponse, PongResponse
from src.application.usecase.create_activity_service import ActivityService

from fastapi import APIRouter, status

router = APIRouter()

activity_service = ActivityService()

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
def activity():
    activity = activity_service.create_activity()
    return CreateActivityResponse(activity_id=activity.id, created_at=activity.created_at)
