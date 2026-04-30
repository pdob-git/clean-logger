from typing import Any, Protocol


class AppLogger(Protocol):
    # noinspection PyUnusedLocal
    def __init__(self, name: str):
        ...

    def debug(self, message: str, **context: Any) -> None:
        ...

    def info(self, message: str, **context: Any) -> None:
        ...

    def warning(self, message: str, **context: Any) -> None:
        ...

    def error(self, message: str, **context: Any) -> None:
        ...
