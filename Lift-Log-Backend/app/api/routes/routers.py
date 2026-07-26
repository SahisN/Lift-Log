from fastapi import APIRouter

base_router = APIRouter()
sys_router = APIRouter(tags=["SYS"])
api_router = APIRouter(prefix="/api/v1")

workout_router = APIRouter(prefix="/workout", tags=["WORKOUT"])

_built = False


def build_router() -> APIRouter:
    from api.routes import sys  # noqa: F401
    from api.routes.v1 import workout  # noqa: F401

    global _built

    if _built:
        return base_router

    api_router.include_router(workout_router)

    base_router.include_router(api_router)
    base_router.include_router(sys_router)

    _built = True
    return base_router


router = build_router()
