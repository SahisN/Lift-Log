from fastapi import APIRouter

base_router = APIRouter()
sys_router = APIRouter(tags=["SYS"])
api_router = APIRouter(prefix="/api/v1")

exercise_router = APIRouter(prefix="/workout", tags=["EXERCISE"])

_built = False


def build_router() -> APIRouter:
    from api.routes import sys  # noqa: F401
    from api.routes.v1 import execrise  # noqa: F401

    global _built

    if _built:
        return base_router

    api_router.include_router(exercise_router)

    base_router.include_router(api_router)
    base_router.include_router(sys_router)

    _built = True
    return base_router


router = build_router()
