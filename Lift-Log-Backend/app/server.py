from contextlib import asynccontextmanager

from api.routes.routers import build_router
from db import (
    get_container_sync_url,
    inject_engine,
    run_alembic_migrations,
    stop_testcontainer,
)
from exception_handler import register_exception_handlers
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    inject_engine()
    sync_url = get_container_sync_url()

    if sync_url:
        run_alembic_migrations(sync_url=sync_url)

    yield
    await stop_testcontainer()


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
_router = build_router()
app.include_router(router=_router)
