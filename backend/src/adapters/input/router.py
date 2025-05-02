from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.adapters.input.http.close_activity import router as close_activity_router
from src.adapters.input.http.create_activity import router as craeate_activity_router
from src.adapters.input.http.evaluation_activity import router as evaluation_activity_router
from src.adapters.input.http.join_activity import router as join_activity_router
from src.adapters.input.http.status_activity import router as status_activity_router
from src.adapters.input.websocket.activity_stream import router as ws_activity_status_router

router = APIRouter()

@router.get("/ping")
def ping():
    return JSONResponse(
        content={"message": "pong"},
        status_code=status.HTTP_200_OK
    )

_activity_router = APIRouter(prefix="/v1")
_activity_router.include_router(craeate_activity_router, tags=["activity"])
_activity_router.include_router(status_activity_router, tags=["activity"])
_activity_router.include_router(join_activity_router, tags=["activity"])
_activity_router.include_router(close_activity_router, tags=["activity"])
_activity_router.include_router(evaluation_activity_router, tags=["activity"])

_activity_router.include_router(ws_activity_status_router)

router.include_router(_activity_router)


