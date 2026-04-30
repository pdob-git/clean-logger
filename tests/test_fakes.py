from typing import Any, List, cast

from clean_logger.application.use_cases.create_order import CreateOrderUseCase
from clean_logger.infrastructure.logging.adapters import PythonLoggerAdapter


class FakeLoggerAdapter(PythonLoggerAdapter):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.messages: List[Any] = []

    def info(self, message: str, **ctx: str) -> None:
        self.messages.append(("INFO", message, ctx))

    debug = warning = error = info


def test_logs_order_created() -> None:
    use_case = CreateOrderUseCase(FakeLoggerAdapter)
    logger = cast(FakeLoggerAdapter, use_case._logger)
    use_case.execute("123")

    assert logger.messages[0][1] == "Creating order"
    print(logger.messages)
