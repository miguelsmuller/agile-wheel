import asyncio
import logging
from uuid import UUID

from google.cloud import firestore
from src.adapters.output.activity_document_mongo import ActivityDocument
from src.application.ports.output.activity_repository import ActivityRepositoryPort
from src.domain.entities.activity import Activity

logger = logging.getLogger(__name__)
logger_prefix = "[ActivityRepositoryFirestoreAdapter]"


class ActivityRepositoryFirestoreAdapter(ActivityRepositoryPort):
    def __init__(self):
        logger.debug("%s Initializing client", logger_prefix)

        self.db = firestore.Client(project="agile-wheel")

        logger.debug("%s client initialized: %s", logger_prefix, str(self.db))

    async def create(self, activity: Activity) -> Activity:
        document = ActivityDocument.from_domain(activity)
        data = document.model_dump()

        doc_ref = self.db.collection("Activities").document(document.app_id)

        logger.debug(
            "%s Attempting to create activity: %s", logger_prefix, str(document)
        )

        try:
            await asyncio.to_thread(doc_ref.set, data)
            logger.debug(
                "%s Successfully created activity: %s", logger_prefix, str(document)
            )
        except Exception as error:
            logger.exception(
                "%s Failed to create activity: %s",
                logger_prefix,
                str(error)
            )
            raise error

        return activity

    async def update(self, activity: Activity) -> Activity:
        document = ActivityDocument.from_domain(activity)
        doc_ref = self.db.collection("Activities").document(document.app_id)

        data = document.model_dump()

        await asyncio.to_thread(doc_ref.set, data)

        return activity

    async def find_one(self, activity_id: UUID) -> Activity | None:
        doc_ref = self.db.collection("Activities").document(str(activity_id))

        doc_snapshot = doc_ref.get()

        if doc_snapshot.exists:
            activity_doc = ActivityDocument.model_validate(doc_snapshot.to_dict())
            return activity_doc.to_domain()

        return None

    async def find_all(self):
        collection_ref = self.db.collection("Activities")

        def _get_all_docs():
            return list(collection_ref.stream())

        docs = await asyncio.to_thread(_get_all_docs)

        activities = []

        for doc in docs:
            activity_doc = ActivityDocument.model_validate(doc.to_dict())
            activities.append(activity_doc.to_domain())

        return activities
