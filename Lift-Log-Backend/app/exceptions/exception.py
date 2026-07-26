class BaseError(Exception):
    status: int = 500
    message: str = "Internal Server Error"

    def __init__(self, custom_msg: str | None = None) -> None:
        self._custom_msg = custom_msg
        super().__init__(
            self._custom_msg if self._custom_msg else self.__class__.message
        )

    def __str__(self) -> str:
        if hasattr(self, "_custom_msg") and self._custom_msg:
            return self._custom_msg

        return self.__class__.message
