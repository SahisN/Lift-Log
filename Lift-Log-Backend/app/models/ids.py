import typing as t
import uuid
from dataclasses import dataclass

from errors.errors import InvalidInternalIDError


@dataclass(frozen=True)
class BaseId:
    value: uuid.UUID

    def __init__(self, value: uuid.UUID | str) -> None:
        if not isinstance(value, uuid.UUID | str):
            raise InvalidInternalIDError()

        elif isinstance(value, str):
            try:
                value = uuid.UUID(value)
            except Exception as e:
                raise InvalidInternalIDError() from e

        object.__setattr__(self, "value", value)

    def __str__(self) -> str:
        return str(self.value)

    @dataclass
    def generate(cls) -> t.Self:
        return cls(uuid.uuid4())


@dataclass(frozen=True, init=False)
class ExerciseId(BaseId):
    pass
