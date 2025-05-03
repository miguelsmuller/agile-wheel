import asyncio
import json
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
from src.adapters.input.websocket.schemas import ActivityStream
from src.adapters.output.activity_repository_adapter import ActivityRepositoryAdapter
from src.application.ports.input.status_activity_port import StatusActivityPort
from src.application.usecase.status_activity_service import StatusActivityService
from src.domain.entities.activity import Activity

MESSAGE_INTERVAL_SECONDS = 1
MESSEGE_TO_DISCONNECT = "close"

router = APIRouter()
repository = ActivityRepositoryAdapter()
service = StatusActivityService(repository=repository)


@router.websocket("/activities/{activity_id}/stream")
async def stream_activity(
    websocket: WebSocket,
    activity_id: UUID = Path(...),
    participant_id: UUID = Query(...),
    status_activity_service: StatusActivityPort = Depends(lambda: service),
) -> None:

    await websocket.accept()

    sender_task = asyncio.create_task(
        _send_activity_periodically(
            websocket,
            status_activity_service,
            activity_id,
            participant_id
        )
    )
    stopper_task = asyncio.create_task(
        _wait_for_disconnect(websocket)
    )

    _, pending = await asyncio.wait(
        [sender_task, stopper_task],
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
            if message.strip().lower() == MESSEGE_TO_DISCONNECT:
                break
    except WebSocketDisconnect as err:
        logging.debug("[ws][wait_for_disconnect] %s", str(err))

async def _send_activity_periodically(
    websocket: WebSocket,
    service: StatusActivityPort,
    activity_id: UUID,
    participant_id: UUID
) -> None:
    while True:
        result = await _safe_fetch_activity(service, activity_id, participant_id)

        message = (
            ActivityStream.from_activity(result).model_dump_json()
            if isinstance(result, Activity)
            else json.dumps(result)
        )

        await websocket.send_text(message)
        await asyncio.sleep(MESSAGE_INTERVAL_SECONDS)


async def _safe_fetch_activity(
    service: StatusActivityPort,
    activity_id: UUID,
    participant_id: UUID
) -> Activity | dict[str, str]:
    try:
        return await service.execute(activity_id, participant_id)

    except Exception as err:
        logging.exception("[ws][safe_fetch_activity] %s", str(err))

        return {
            "type": "error",
            "error": {"message": str(err), "code": "internal_error"},
        }
