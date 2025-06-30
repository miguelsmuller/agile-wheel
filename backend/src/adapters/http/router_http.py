from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.adapters.http.get_result_activity import endpoint as result_activity_endpoint
from src.adapters.http.get_status_activity import endpoint as status_activity_endpoint
from src.adapters.http.patch_join_activity import endpoint as join_activity_endpoint
from src.adapters.http.post_close_activity import endpoint as close_activity_endpoint
from src.adapters.http.post_create_activity import endpoint as craeate_activity_endpoint
from src.adapters.http.post_evaluation_activity import endpoint as evaluation_activity_endpoint

router_http = APIRouter()

@router_http.get("/ping")
def ping():
    return JSONResponse(
        content={"message": "pong"},
        status_code=status.HTTP_200_OK
    )

_activity_router = APIRouter(prefix="/v1")
_activity_router.include_router(craeate_activity_endpoint, tags=["activity"])
_activity_router.include_router(status_activity_endpoint, tags=["activity"])
_activity_router.include_router(join_activity_endpoint, tags=["activity"])
_activity_router.include_router(close_activity_endpoint, tags=["activity"])
_activity_router.include_router(evaluation_activity_endpoint, tags=["activity"])
_activity_router.include_router(result_activity_endpoint, tags=["activity"])

router_http.include_router(_activity_router)
