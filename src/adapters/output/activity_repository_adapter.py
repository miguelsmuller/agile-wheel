from src.adapters.output.schema.activity_document_mongo import ActivityDocument

from src.application.domain.models.activity import Activity
from src.application.ports.output.activity_repository import ActivityRepositoryPort

class ActivityRepositoryAdapter(ActivityRepositoryPort):
    async def save(self, activity: Activity) -> None:
        doc = ActivityDocument.from_domain(activity)
        
        activity_document = await doc.insert()
        activity = activity_document.to_domain()
        
        return activity

    async def find_all(self):
        docs = await ActivityDocument.find_all().to_list()
        return [doc.to_domain() for doc in docs]
