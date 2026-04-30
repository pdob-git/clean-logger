from typing import Protocol, Any


class AppLogger(Protocol):
    def debug(self, message: str, **context: Any) -> None:
        ...

    def info(self, message: str, **context: Any) -> None:
        ...

    def warning(self, message: str, **context: Any) -> None:
        ...

    def error(self, message: str, **context: Any) -> None:
        ...