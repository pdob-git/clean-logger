import logging
from typing import Any


class PythonLoggerAdapter:
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)

    def debug(self, message: str, **context: Any) -> None:
        self._logger.debug(
            message,
            extra={"context": context}
        )

    def info(self, message: str, **context: Any) -> None:
        self._logger.info(
            f"{message} | {context}"
        )

    def warning(self, message: str, **context: Any) -> None:
        self._logger.warning(
            f"{message} | {context}"
        )

    def error(self, message: str, **context: Any) -> None:
        self._logger.error(
            f"{message} | {context}"
        )