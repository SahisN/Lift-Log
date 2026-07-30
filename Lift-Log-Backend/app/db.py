import typing as t
from functools import lru_cache

from deps import inject_app_settings
from fastapi import Depends
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

_container: t.Any = None
_container_sync_url: str | None = None


def _start_testcontainer() -> str:
    global _container, _container_sync_url

    from testcontainers.postgres import PostgresContainer

    _container = PostgresContainer("postgres:17-alpine")
    try:
        _container.start()
    except Exception as exec:
        raise RuntimeError(
            "Failed to start Postgres testcontainer. Is Docker running? check (`docker ps`)"
        ) from exec

    raw_url: str = make_url(_container.get_connection_url())
    async_url = raw_url.set(drivername="postgresql+asyncpg")
    sync_url = raw_url.set(drivername="postgresql+psycopg")

    _container_sync_url = sync_url.render_as_string(hide_password=False)

    print("ASYNC_DATABASE_URL not set, starting testcontainer")

    return async_url.render_as_string(hide_password=False)


def get_container_sync_url() -> str | None:
    return _container_sync_url


@lru_cache
def inject_engine() -> None:
    settings = inject_app_settings()
    url = settings.secrets.async_database_url.get_secret_value()
    if not url:
        url = _start_testcontainer()
    return create_async_engine(url)


@lru_cache
def _inject_session_factory() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        inject_engine(), class_=AsyncSession, expire_on_commit=False
    )


def inject_session_factory() -> async_sessionmaker[AsyncSession]:
    return _inject_session_factory()


async def inject_postgres_session(
    factory: async_sessionmaker[AsyncSession] = Depends(_inject_session_factory),  # noqa: B008
) -> t.AsyncGenerator[AsyncSession, None]:
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def stop_testcontainer() -> None:
    global _container, _container_sync_url

    inject_engine.cache_clear()
    _inject_session_factory.cache_clear()

    if _container is not None:
        print("Stopping testcontainer")
        _container.stop()
        _container = None
        _container_sync_url = None
