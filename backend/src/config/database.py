import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.adapters.persistence.activity_document import ActivityDocumentForMongo

logger = logging.getLogger(__name__)

async def initialize_database(host, port):
    log_data = { host: host, port: port }
    logger.debug("[INIT_DATABASE] Initializing the database", extra=log_data)

    try:
        client = AsyncIOMotorClient(f"mongodb://{host}:{port}")

        await init_beanie(
            database=client.mydb,
            document_models=[
                ActivityDocumentForMongo
            ]
        )

        logger.debug("[INIT_DATABASE] Database initialized")

    except Exception as err:
        log_data = { "error": str(err) }
        logger.error("[INIT_DATABASE] Database initialization failed", extra=log_data)
