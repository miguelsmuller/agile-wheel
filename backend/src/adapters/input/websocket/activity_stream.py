from fastapi import APIRouter, WebSocket
import asyncio
import random
import json


router = APIRouter()

@router.websocket("/activity-stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_text(
                json.dumps({
                    "value": random.randint(1, 100),
                })
            )
            await asyncio.sleep(1)
    except Exception as e:
        pass
