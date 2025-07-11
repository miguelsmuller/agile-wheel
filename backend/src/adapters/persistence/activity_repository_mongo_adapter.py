from uuid import UUID

from src.adapters.persistence.activity_document import ActivityDocumentForMongo
from src.application.ports.output.activity_repository import ActivityRepositoryPort
from src.domain.entities.activity import Activity
from src.domain.exceptions import ActivityNotFoundError


class ActivityRepositoryAdapter(ActivityRepositoryPort):
    def __init__(self):
        self._cache: dict[str, ActivityDocumentForMongo] = {}

    async def create(self, activity: Activity) -> Activity:
        activity_document = ActivityDocumentForMongo.from_domain(activity)
        await activity_document.insert()

        return activity_document.to_domain()

    async def update(self, activity: Activity) -> Activity:
        cached_doc = self._cache.get(str(activity.id))
        if not cached_doc:
            # fallback caso update seja chamado isoladamente
            cached_doc = await ActivityDocumentForMongo.find_one(
                ActivityDocumentForMongo.app_id == str(activity.id)
            )

            if not cached_doc:
                raise ActivityNotFoundError("Activity not found for update")

        activity_doc = ActivityDocumentForMongo.from_domain(activity)
        activity_doc.id = cached_doc.id

        await activity_doc.save()

        return activity_doc.to_domain()

    async def find_one(self, activity_id: UUID) -> Activity | None:
        activity_document = await ActivityDocumentForMongo.find_one(
            ActivityDocumentForMongo.app_id == str(activity_id)
        )

        if activity_document:
            self._cache[str(activity_id)] = activity_document
            return activity_document.to_domain()
        return None

    async def find_all(self):
        docs = await ActivityDocumentForMongo.find_all().to_list()
        return [doc.to_domain() for doc in docs]
