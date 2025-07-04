from unittest.mock import AsyncMock, patch

import pytest

from src.adapters.persistence.activity_document import ActivityDocumentForMongo
from src.config.database import initialize_database


@pytest.fixture
def mock_dependencies():
    mock_client = AsyncMock()
    mock_init_beanie = AsyncMock()

    with (
        patch(
            "src.config.database.AsyncIOMotorClient",
            return_value=mock_client
        ) as mock_motor_client,
        patch(
            "src.config.database.init_beanie",
            mock_init_beanie
        )
    ):
        yield mock_client, mock_init_beanie, mock_motor_client


@pytest.fixture
def mock_logger():
    with patch("src.config.database.logger") as mock:
        yield mock


@pytest.mark.asyncio
async def test_init_database_success(mock_dependencies):
    # Given
    mock_client, mock_init_beanie, mock_motor_client = mock_dependencies

    # When
    await initialize_database(host="localhost", port=27017)

    # Then
    mock_motor_client.assert_called_once_with("mongodb://localhost:27017")
    mock_init_beanie.assert_awaited_once_with(
        database=mock_client.mydb,
        document_models=[ActivityDocumentForMongo]
    )


@pytest.mark.asyncio
async def test_init_database_failure(mock_dependencies, mock_logger):
    # Given
    mock_client, mock_init_beanie, mock_motor_client = mock_dependencies
    mock_init_beanie.side_effect = Exception("Database initialization failed")

    # When
    await initialize_database(host="localhost", port=27017)

    # Then
    mock_motor_client.assert_called_once_with("mongodb://localhost:27017")
    mock_init_beanie.assert_awaited_once()

    mock_logger.error.assert_called_once()
    log_messages = [call.args[0] for call in mock_logger.error.call_args_list]
    assert "[INIT_DATABASE] Database initialization failed" in log_messages
