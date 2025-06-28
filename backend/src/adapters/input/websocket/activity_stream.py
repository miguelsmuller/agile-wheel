import asyncio
import json
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from pydantic.json import pydantic_encoder
from src.adapters.input.websocket.schemas import ActivityStream, ActivityStreamType
from src.application.ports.input.get_activity_port import GetActivityPort
from src.config.dependencies import get_status_activity_service
from src.domain.entities.activity import Activity

MESSAGE_INTERVAL_SECONDS = 1
MESSAGE_TO_DISCONNECT = "close"

router = APIRouter()

@router.websocket("/activities/{activity_id}/stream")
async def stream_activity(
    websocket: WebSocket,
    activity_id: UUID = Path(...),
    participant_id: UUID = Query(...),
    status_activity_service: GetActivityPort = Depends(get_status_activity_service),
) -> None:
    await websocket.accept()

    send_task = asyncio.create_task(
        _send_activity_periodically(
            websocket,
            status_activity_service,
            activity_id,
            participant_id
        )
    )
    disconnect_task = asyncio.create_task(_wait_for_disconnect(websocket))

    _, pending = await asyncio.wait(
        [send_task, disconnect_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

    if websocket.client_state == WebSocketState.CONNECTED:
        await websocket.close()


async def _wait_for_disconnect(websocket: WebSocket) -> None:
    try:
        while True:
            message = await websocket.receive_text()
            if message.strip().lower() == MESSAGE_TO_DISCONNECT:
                break
    except WebSocketDisconnect as err:
        logging.debug("[ws][wait_for_disconnect] %s", str(err))


async def _send_activity_periodically(
    websocket: WebSocket,
    service: GetActivityPort,
    activity_id: UUID,
    participant_id: UUID
) -> None:
    while True:
        payload = await _build_payload(service, activity_id, participant_id)
        await websocket.send_text(payload)
        await asyncio.sleep(MESSAGE_INTERVAL_SECONDS)


async def _build_payload(
    service: GetActivityPort,
    activity_id: UUID,
    participant_id: UUID
) -> str:
    try:
        result = await service.execute(activity_id, participant_id)
        if isinstance(result, Activity):
            message = {
                "type": (
                    ActivityStreamType.UPDATE if result.is_opened else ActivityStreamType.CLOSE
                ),
                "activity_id": str(result.id),
                "activity": ActivityStream.from_activity(result).model_dump()
            }
        else:
            raise ValueError("result is not of type Activity")

    except Exception as err:
        logging.exception("[ws][safe_fetch_activity] %s", str(err))

        message = {
            "type": ActivityStreamType.ERROR,
            "activity_id": activity_id,
            "detail": str(err)
        }

    return json.dumps(message, default=pydantic_encoder)
