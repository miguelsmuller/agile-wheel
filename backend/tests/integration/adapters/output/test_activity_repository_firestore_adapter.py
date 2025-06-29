from unittest.mock import MagicMock, patch

import pytest
from src.adapters.output.activity_repository_firestore_adapter import (
    ActivityRepositoryFirestoreAdapter,
)


@pytest.fixture
def mock_firestore_client():
    firestore_client_path = (
        "src.adapters.output.activity_repository_firestore_adapter.firestore.Client"
    )
    with patch(firestore_client_path) as mock_client:
        yield mock_client


@pytest.mark.asyncio
async def test_create_activity_firestore(
    mock_firestore_client, mock_activity_fixture, mock_activity_document_fixture
):
    # Given
    mock_client_instance = MagicMock()
    mock_firestore_client.return_value = mock_client_instance

    mock_collection = MagicMock()
    mock_client_instance.collection.return_value = mock_collection

    mock_doc_ref = MagicMock()
    mock_doc_ref.set = MagicMock()
    mock_collection.document.return_value = mock_doc_ref

    adapter = ActivityRepositoryFirestoreAdapter()

    # When
    result = await adapter.create(mock_activity_fixture)

    # Then
    mock_client_instance.collection.assert_called_once_with("Activities")
    mock_collection.document.assert_called_once_with(mock_activity_document_fixture.app_id)
    mock_doc_ref.set.assert_called_once()
    assert result == mock_activity_fixture


@pytest.mark.asyncio
async def test_update_activity_firestore(
    mock_firestore_client, mock_activity_fixture, mock_activity_document_fixture
):
    # Given
    mock_client_instance = MagicMock()
    mock_firestore_client.return_value = mock_client_instance

    mock_collection = MagicMock()
    mock_client_instance.collection.return_value = mock_collection

    mock_doc_ref = MagicMock()
    mock_doc_ref.set = MagicMock()
    mock_collection.document.return_value = mock_doc_ref

    adapter = ActivityRepositoryFirestoreAdapter()

    # When
    result = await adapter.update(mock_activity_fixture)

    # Then
    mock_client_instance.collection.assert_called_once_with("Activities")
    mock_collection.document.assert_called_once_with(mock_activity_document_fixture.app_id)
    mock_doc_ref.set.assert_called_once()
    assert result == mock_activity_fixture


@pytest.mark.asyncio
async def test_find_one_activity_exists(
    mock_firestore_client, mock_activity_fixture, mock_activity_document_fixture
):
    # Given
    mock_client_instance = MagicMock()
    mock_firestore_client.return_value = mock_client_instance

    mock_collection = MagicMock()
    mock_client_instance.collection.return_value = mock_collection

    mock_doc_ref = MagicMock()
    mock_collection.document.return_value = mock_doc_ref

    mock_doc_snapshot = MagicMock()
    mock_doc_snapshot.exists = True
    mock_doc_snapshot.to_dict.return_value = mock_activity_document_fixture.model_dump()
    mock_doc_ref.get.return_value = mock_doc_snapshot

    adapter = ActivityRepositoryFirestoreAdapter()

    # When
    result = await adapter.find_one(mock_activity_fixture.id)

    # Then
    mock_client_instance.collection.assert_called_once_with("Activities")
    mock_collection.document.assert_called_once_with(mock_activity_document_fixture.app_id)
    mock_doc_ref.get.assert_called_once()
    assert result.id == mock_activity_fixture.id

@pytest.mark.asyncio
async def test_find_one_activity_not_found(mock_firestore_client, mock_activity_fixture):
    # Given
    mock_client_instance = MagicMock()
    mock_firestore_client.return_value = mock_client_instance

    mock_collection = MagicMock()
    mock_client_instance.collection.return_value = mock_collection

    mock_doc_ref = MagicMock()
    mock_collection.document.return_value = mock_doc_ref

    mock_doc_snapshot = MagicMock()
    mock_doc_snapshot.exists = False
    mock_doc_ref.get.return_value = mock_doc_snapshot

    adapter = ActivityRepositoryFirestoreAdapter()

    # When
    result = await adapter.find_one(mock_activity_fixture.id)

    # Then
    assert result is None

@pytest.mark.asyncio
async def test_find_all_activities(
    mock_firestore_client, mock_activity_fixture, mock_activity_document_fixture
):
    # Given
    mock_client_instance = MagicMock()
    mock_firestore_client.return_value = mock_client_instance

    mock_collection = MagicMock()
    mock_client_instance.collection.return_value = mock_collection

    mock_doc1 = MagicMock()
    mock_doc1.to_dict.return_value = mock_activity_document_fixture.model_dump()

    mock_doc2 = MagicMock()
    mock_doc2.to_dict.return_value = mock_activity_document_fixture.model_dump()

    mock_collection.stream.return_value = [mock_doc1, mock_doc2]

    adapter = ActivityRepositoryFirestoreAdapter()

    # When
    results = await adapter.find_all()

    # Then
    assert len(results) == 2
    assert all(r.id == mock_activity_fixture.id for r in results)
