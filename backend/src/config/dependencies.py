import logging

from fastapi import Depends

from src.adapters.persistence.activity_repository_firestore_adapter import (
    ActivityRepositoryFirestoreAdapter,
)
from src.adapters.persistence.activity_repository_mongo_adapter import ActivityRepositoryAdapter
from src.application.usecase import (
    CloseActivityService,
    CreateActivityService,
    EvaluationActivityService,
    GetActivityResultService,
    GetActivityStatusService,
    JoinActivityService,
)
from src.config.settings import initialize_settings

logger = logging.getLogger(__name__)

def get_activity_repository():
    settings = initialize_settings()

    default_repository = ActivityRepositoryAdapter

    repository_mapping = {
        "firestore": ActivityRepositoryFirestoreAdapter,
    }

    repository = repository_mapping.get(settings.db_type, default_repository)

    return repository()


def get_create_activity_service(
    repository=Depends(get_activity_repository)
):
    return CreateActivityService(repository=repository)


def get_close_activity_service(
    repository=Depends(get_activity_repository)
):
    return CloseActivityService(repository=repository)


def get_evaluation_activity_service(
    repository=Depends(get_activity_repository)
):
    return EvaluationActivityService(repository=repository)


def get_join_activity_service(
    repository=Depends(get_activity_repository)
):
    return JoinActivityService(repository=repository)


def get_status_activity_service(
    repository=Depends(get_activity_repository)
):
    return GetActivityStatusService(repository=repository)

def get_result_activity_service(
    repository=Depends(get_activity_repository)
):
    return GetActivityResultService(repository=repository)

