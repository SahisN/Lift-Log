from fastapi import status

from api.routes.routers import sys_router


@sys_router.get("/", status_code=status.HTTP_200_OK)
async def alive_check() -> dict[str, str]:
    return {"status": "alive"}


@sys_router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}
