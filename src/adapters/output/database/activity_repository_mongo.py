from src.application.ports.output.database.activity_repository import ActivityRepository
from src.application.domain.models.activity import Activity
from .activity_document_mongo import ActivityDocument

class ActivityRepositoryMongo(ActivityRepository):
    async def save(self, activity: Activity) -> None:
        doc = ActivityDocument.from_domain(activity)
        
        activity_document = await doc.insert()

        activity = activity_document.to_domain()
        
        return activity

    async def find_all(self):
        docs = await ActivityDocument.find_all().to_list()
        return [doc.to_domain() for doc in docs]
