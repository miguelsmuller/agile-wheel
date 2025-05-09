from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.input.router import router
from src.config.database import initialize_database
from src.config.logger import initialize_logger
from src.config.monitoring import initialize_monitoring
from src.config.settings import get_settings

initialize_logger()
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = settings

    await initialize_database(settings.db_host, settings.db_port)
    await initialize_monitoring(settings)

    yield

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app

app = create_app()
