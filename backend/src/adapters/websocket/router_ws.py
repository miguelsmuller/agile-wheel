from fastapi import APIRouter
from src.adapters.websocket.activity_stream import router as ws_activity_status_router

ws_router = APIRouter(prefix="/v1")

ws_router.include_router(ws_activity_status_router)
