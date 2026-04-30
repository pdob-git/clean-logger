import uuid

from ..infrastructure.logging.config import configure_logging
from ..infrastructure.logging.listener import start_listener
from ..infrastructure.logging.context import correlation_id

from ..infrastructure.logging.adapters import PythonLoggerAdapter
from ..application.use_cases.create_order import CreateOrderUseCase



def main() -> None:
    configure_logging()
    start_listener()

    correlation_id.set(str(uuid.uuid4()))

    logger = PythonLoggerAdapter(__name__)
    logger.info(f"Program started")

    use_case = CreateOrderUseCase(
        logger_provider=PythonLoggerAdapter
    )

    use_case.execute("ORD-123")
    logger.info(f"Program completed")

if __name__ == "__main__":
    main()