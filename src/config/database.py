from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.adapters.output.activity_document_mongo import ActivityDocument


async def init_database(host, port):
    client = AsyncIOMotorClient(f"mongodb://{host}:{port}")

    await init_beanie(
        database=client.mydb,
        document_models=[
            ActivityDocument
        ]
    )
