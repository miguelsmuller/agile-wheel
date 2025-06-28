
from unittest.mock import MagicMock

from src.adapters.output.activity_repository_firestore_adapter import (
    ActivityRepositoryFirestoreAdapter,
)
from src.adapters.output.activity_repository_mongo_adapter import ActivityRepositoryAdapter
from src.application.usecase.close_activity_service import CloseActivityService
from src.application.usecase.create_activity_service import CreateActivityService
from src.application.usecase.evaluation_activity_service import EvaluationActivityService
from src.application.usecase.join_activity_service import JoinActivityService
from src.application.usecase.get_activity_service import StatusActivityService
from src.config.dependencies import (
    get_activity_repository,
    get_close_activity_service,
    get_create_activity_service,
    get_evaluation_activity_service,
    get_join_activity_service,
    get_status_activity_service,
)


def test_get_activity_repository_default():
    # when
    repository = get_activity_repository()

    # then
    assert isinstance(repository, ActivityRepositoryAdapter)


def test_get_activity_repository_firestore(mocker):
    # given
    mock_settings = MagicMock()
    mock_settings.db_type = "firestore"
    mocker.patch("src.config.dependencies.initialize_settings", return_value=mock_settings)
    mocker.patch("src.adapters.output.activity_repository_firestore_adapter.firestore.Client")

    # when
    repository = get_activity_repository()
    assert isinstance(repository, ActivityRepositoryFirestoreAdapter)


def test_get_create_activity_service():
    # given
    service = get_create_activity_service()

    # then
    assert isinstance(service, CreateActivityService)


def test_get_close_activity_service():
    # given
    service = get_close_activity_service()

    # then
    assert isinstance(service, CloseActivityService)


def test_get_evaluation_activity_service():
    # given
    service = get_evaluation_activity_service()

    # then
    assert isinstance(service, EvaluationActivityService)


def test_get_join_activity_service():
    # given
    service = get_join_activity_service()

    # then
    assert isinstance(service, JoinActivityService)


def test_get_status_activity_service():
    # given
    service = get_status_activity_service()

    # then
    assert isinstance(service, StatusActivityService)
