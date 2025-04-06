from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.adapters.input.router import router
from src.config.database import init_database
from src.config.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = get_settings()

    await init_database(
        app.state.settings.db_host,
        app.state.settings.db_port
    )

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)

