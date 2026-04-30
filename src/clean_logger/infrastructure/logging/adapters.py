import logging
from typing import Any

from ...application.ports.logger import AppLogger


class PythonLoggerAdapter(AppLogger):
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)

    def debug(self, message: str, **context: Any) -> None:
        self._logger.debug(message, extra={"context": context} if context else {})

    def info(self, message: str, **context: Any) -> None:
        self._logger.info(message, extra={"context": context} if context else {})

    def warning(self, message: str, **context: Any) -> None:
        self._logger.warning(message, extra={"context": context} if context else {})

    def error(self, message: str, **context: Any) -> None:
        self._logger.error(message, extra={"context": context} if context else {})
