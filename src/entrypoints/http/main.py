from re import A
from fastapi import FastAPI

from src.adapters.input.http.router import router


app = FastAPI()

app.include_router(router)

