from ..ports.logger import AppLogger

from typing import Callable

LoggerProvider = Callable[[str], "AppLogger"]

class CreateOrderUseCase:
    def __init__(self, logger_provider:  LoggerProvider):
        self._logger = logger_provider(__name__)

    def execute(self, order_id: str) -> None:
        self._logger.info(
            "Creating order",
            order_id=order_id
        )

        # business logic here

        self._logger.info(
            "Order created",
            order_id=order_id
        )