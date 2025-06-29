from typing import TYPE_CHECKING

import pytest
from src.adapters.persistence.activity_document import ActivityDocument

if TYPE_CHECKING:
    from src.domain.entities.activity import Activity


@pytest.mark.asyncio
async def test_activity_document_from_domain(mock_activity_fixture):
    # Given
    activity_data: Activity = mock_activity_fixture

    # When
    activity_document = ActivityDocument.from_domain(activity_data)

    # Then
    assert activity_document.app_id == str(activity_data.id)
    assert activity_document.created_at == activity_data.created_at
    assert activity_document.is_opened == activity_data.is_opened
    assert len(activity_document.participants) == len(activity_data.participants)
    assert len(activity_document.dimensions) == len(activity_data.dimensions)
    assert len(activity_document.evaluations) == len(activity_data.evaluations)


@pytest.mark.asyncio
async def test_activity_document_to_domain(mock_activity_document_fixture):
    # Given
    activity_document:ActivityDocument = mock_activity_document_fixture

    # When
    activity_domain = activity_document.to_domain()

    # Then
    assert str(activity_domain.id) == str(activity_document.app_id)
    assert activity_domain.created_at == activity_document.created_at
    assert activity_domain.is_opened == activity_document.is_opened
    assert len(activity_domain.participants) == len(activity_document.participants)
    assert len(activity_domain.dimensions) == len(activity_document.dimensions)
    assert len(activity_domain.evaluations) == len(activity_document.evaluations)
