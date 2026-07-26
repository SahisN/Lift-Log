from exceptions.exception import BaseError
from fastapi import Request
from fastapi.responses import JSONResponse


def register_exception_handlers(app):
    @app.exception_handler(BaseError)
    async def _handle_base_exception(
        _request: Request, error: BaseError
    ) -> JSONResponse:
        return JSONResponse(status_code=error.status, content={"detail": str(error)})
