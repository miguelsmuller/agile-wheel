from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.adapters.input.router import router
from src.config.database import init_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)

