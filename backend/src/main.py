from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.http.router_http import router_http
from src.adapters.websocket.router_ws import router_ws
from src.config.database import initialize_database
from src.config.logger import initialize_logger
from src.config.monitoring import initialize_monitoring
from src.config.settings import initialize_settings

initialize_logger()
settings = initialize_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = settings

    await initialize_database(settings.db_host, settings.db_port)
    await initialize_monitoring(settings)

    yield

def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/docs" if settings.enable_docs else None,
        redoc_url="/redoc" if settings.enable_docs else None,
        openapi_url="/openapi.json" if settings.enable_docs else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router_http)
    app.include_router(router_ws)

    return app

app = create_app()
