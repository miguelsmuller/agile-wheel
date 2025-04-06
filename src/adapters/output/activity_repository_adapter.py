from src.adapters.output.schema.activity_document_mongo import ActivityDocument
from src.application.domain.models.activity import Activity
from src.application.ports.output.activity_repository import ActivityRepositoryPort


class ActivityRepositoryAdapter(ActivityRepositoryPort):
    async def save(self, activity: Activity) -> Activity:
        return await self._upsert(activity, None)

    async def update(self, activity: Activity, update_callback: callable) -> Activity:
        return await self._upsert(activity, update_callback)

    async def _upsert(self, activity: Activity, update_callback: callable) -> Activity:
        activity_document = await ActivityDocument.find_one(
            ActivityDocument.app_id == str(activity.id)
        )

        if activity_document:
            update_callback(activity_document)
            await activity_document.save()
        else:
            activity_document = ActivityDocument.from_domain(activity)
            await activity_document.insert()

        return activity_document.to_domain()

    async def find_all(self):
        docs = await ActivityDocument.find_all().to_list()
        return [doc.to_domain() for doc in docs]
