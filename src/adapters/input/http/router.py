from fastapi import APIRouter, status
from pydantic import BaseModel


router = APIRouter()


class PongResponse(BaseModel):
    message: str

@router.get("/")
def read_root():
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
