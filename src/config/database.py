from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.adapters.output.schema.activity_document_mongo import ActivityDocument

async def init_database():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    
    await init_beanie(database=client.mydb, document_models=[ActivityDocument])
