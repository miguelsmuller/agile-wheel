import logging

from fastapi import Depends
from src.adapters.output.activity_repository_firestore_adapter import (
    ActivityRepositoryFirestoreAdapter,
)
from src.adapters.output.activity_repository_mongo_adapter import ActivityRepositoryAdapter
from src.application.usecase.close_activity_service import CloseActivityService
from src.application.usecase.create_activity_service import CreateActivityService
from src.application.usecase.evaluation_activity_service import EvaluationActivityService
from src.application.usecase.join_activity_service import JoinActivityService
from src.application.usecase.status_activity_service import StatusActivityService
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
    return StatusActivityService(repository=repository)

