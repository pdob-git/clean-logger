import uuid

from ..application.use_cases.create_order import CreateOrderUseCase
from ..infrastructure.logging.adapters import PythonLoggerAdapter
from ..infrastructure.logging.config import configure_logging
from ..infrastructure.logging.context import correlation_id
from ..infrastructure.logging.listener import start_listener


def main() -> None:
    configure_logging()
    start_listener()

    correlation_id.set(str(uuid.uuid4()))

    logger = PythonLoggerAdapter(__name__)
    logger.info("Program started")

    use_case = CreateOrderUseCase(logger_provider=PythonLoggerAdapter)

    use_case.execute("ORD-123")
    logger.info("Program completed")


if __name__ == "__main__":
    main()
