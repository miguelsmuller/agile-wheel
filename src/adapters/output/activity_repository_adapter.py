from uuid import UUID

from src.adapters.output.activity_document_mongo import ActivityDocument
from src.application.ports.output.activity_repository import ActivityRepositoryPort
from src.domain.entities.activity import Activity


class ActivityRepositoryAdapter(ActivityRepositoryPort):
    async def create(self, activity: Activity) -> Activity:
        activity_document = ActivityDocument.from_domain(activity)
        await activity_document.insert()

        return activity_document.to_domain()

    async def update(self, activity: Activity, update_callback: callable) -> Activity:
        activity_document = await ActivityDocument.find_one(
            ActivityDocument.app_id == str(activity.id)
        )

        if not activity_document:
            raise LookupError("Activity not found")

        update_callback(activity_document)
        await activity_document.save()

        return activity_document.to_domain()

    async def find_one(self, activity_id: UUID) -> Activity | None:
        activity_document = await ActivityDocument.find_one(
            ActivityDocument.app_id == str(activity_id)
        )

        if activity_document:
            return activity_document.to_domain()
        return None

    async def find_all(self):
        docs = await ActivityDocument.find_all().to_list()
        return [doc.to_domain() for doc in docs]
