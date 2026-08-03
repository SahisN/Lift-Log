from .base_error import BaseError


class InvalidInternalIDError(BaseError):
    status: int = 400
    message: str = "Invalid Internal ID"


class ExerciseNotFound(BaseError):
    status: int = 404
    message: str = "Exercise Not Found"


class ExerciseProfileNotFound(BaseError):
    status: int = 404
    message: str = "Exercise Profile Not Found"
