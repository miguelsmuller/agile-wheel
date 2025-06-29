from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.adapters.http.close_activity import router as close_activity_router
from src.adapters.http.create_activity import router as craeate_activity_router
from src.adapters.http.evaluation_activity import router as evaluation_activity_router
from src.adapters.http.join_activity import router as join_activity_router
from src.adapters.http.result_activity import router as result_activity_router
from src.adapters.http.status_activity import router as status_activity_router

http_router = APIRouter()

@http_router.get("/ping")
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
_activity_router.include_router(result_activity_router, tags=["activity"])

http_router.include_router(_activity_router)
