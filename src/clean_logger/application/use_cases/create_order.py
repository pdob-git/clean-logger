from ..ports.logger import AppLogger


class CreateOrderUseCase:
    def __init__(self, logger: AppLogger):
        self._logger = logger

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