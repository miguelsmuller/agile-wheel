import json
from uuid import UUID

import pytest
import src.adapters.websocket.activity_stream as stream_mod
from fastapi.testclient import TestClient
from src.adapters.websocket.schemas import ActivityStreamType
from src.config.dependencies import get_status_activity_service
from src.domain.entities.activity import Activity
from src.domain.entities.participant import Participant
from src.main import app

ACTIVITY_ID = UUID("8e6587b8-b158-4068-a254-76bd0d31f4f7")
PARTICIPANT_ID = UUID("7870b158-4900-466a-948c-14b462b62f5b")

@pytest.fixture(autouse=True)
def clear_overrides_and_shorten_interval():
    app.dependency_overrides.clear()

    original_interval = stream_mod.MESSAGE_INTERVAL_SECONDS

    stream_mod.MESSAGE_INTERVAL_SECONDS = 0
    yield
    stream_mod.MESSAGE_INTERVAL_SECONDS = original_interval

    app.dependency_overrides.clear()


@pytest.mark.parametrize(
    "is_opened, expected_type",
    [
        (True, ActivityStreamType.UPDATE.value),
        (False, ActivityStreamType.CLOSE.value),
    ],
)
def test_stream_activity_status_updates_and_closes(is_opened, expected_type):
    # Given
    activity = Activity(is_opened=is_opened)
    owner = Participant(name="Owner", email="owner@example.com", role="owner")
    activity.participants.append(owner)

    class DummyService:
        async def get_activity_status(self, activity_id, participant_id):
            return activity

    app.dependency_overrides[get_status_activity_service] = lambda: DummyService()

    client = TestClient(app)

    # When / Then
    with client.websocket_connect(
        f"/v1/activities/{ACTIVITY_ID}/stream?participant_id={PARTICIPANT_ID}"
    ) as ws:
        text = ws.receive_text()
        msg = json.loads(text)

        assert msg["type"] == expected_type
        assert msg["activity_id"] == str(activity.id)

        activity_payload = msg["activity"]
        assert activity_payload["is_opened"] is is_opened

        parts = activity_payload["participants"]
        assert isinstance(parts, list) and parts

        ws.send_text("close")


def test_stream_activity_error_path():
    # Given
    class ErrorService:
        async def get_activity_status(self, activity_id, participant_id):
            raise RuntimeError("fetch failed")

    app.dependency_overrides[get_status_activity_service] = lambda: ErrorService()

    client = TestClient(app)

    # When / Then
    with client.websocket_connect(
        f"/v1/activities/{ACTIVITY_ID}/stream?participant_id={PARTICIPANT_ID}"
    ) as ws:
        text = ws.receive_text()
        msg = json.loads(text)

        assert msg["type"] == ActivityStreamType.ERROR.value

        assert msg["activity_id"] == str(ACTIVITY_ID)
        assert "fetch failed" in msg.get("detail", "")

        ws.send_text("close")
