import asyncio
import json
import random

from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.websocket("/activity-stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_text(
                json.dumps({
                    "value": random.randint(1, 100),  # noqa: S311
                })
            )
            await asyncio.sleep(1)
    except Exception:  # noqa: S110
        pass
