import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.adapters.output.activity_document import ActivityDocument

logger = logging.getLogger(__name__)

async def initialize_database(host, port):
    logger.debug("[init_database] Initializing the database")

    try:
        client = AsyncIOMotorClient(f"mongodb://{host}:{port}")

        await init_beanie(
            database=client.mydb,
            document_models=[
                ActivityDocument
            ]
        )

        logger.debug("[init_database] Database initialized")

    except Exception as err:
        logger.error("[init_database] %s", str(err))
