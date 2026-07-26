from contextlib import asynccontextmanager

from api.routes.routers import build_router
from exception_handler import register_exception_handlers
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
_router = build_router()
app.include_router(router=_router)
