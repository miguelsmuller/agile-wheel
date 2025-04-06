from fastapi import APIRouter, status
from src.adapters.input.close_activity import router as close_activity_router
from src.adapters.input.create_activity import router as craeate_activity_router
from src.adapters.input.join_activity import router as join_activity_router
from src.adapters.input.schemas import PongResponse

router = APIRouter()

@router.get("/")
def root():
    return {"Hello": "World"}

@router.get(
    "/ping",
    responses={status.HTTP_200_OK: {"description": "Return a pong message"}},
    response_model=PongResponse
)
def ping():
    return PongResponse(message="pong")

_activity_router = APIRouter(prefix="/v1")
_activity_router.include_router(craeate_activity_router, tags=["activity"])
_activity_router.include_router(join_activity_router, tags=["activity"])
_activity_router.include_router(close_activity_router, tags=["activity"])

router.include_router(_activity_router)


