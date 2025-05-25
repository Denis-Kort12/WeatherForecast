from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.router import router

app = FastAPI()

app.mount('/static', StaticFiles(directory='src/static'), 'static')

app.include_router(router)