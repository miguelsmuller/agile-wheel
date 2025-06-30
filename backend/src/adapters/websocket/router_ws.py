from fastapi import APIRouter
from src.adapters.websocket.ws_activity_stream import endpoint as ws_activity_status_endpoint

router_ws = APIRouter(prefix="/v1")

router_ws.include_router(ws_activity_status_endpoint)
