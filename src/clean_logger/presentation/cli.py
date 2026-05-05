import time
import uuid

from ..application.use_cases.create_order import CreateOrderUseCase
from ..infrastructure.logging.adapters import PythonLoggerAdapter
from ..infrastructure.logging.config import configure_logging
from ..infrastructure.logging.context import correlation_id


def action(logger: PythonLoggerAdapter) -> None:
    logger.info("Program started")

    use_case = CreateOrderUseCase(logger_provider=PythonLoggerAdapter)

    use_case.execute("ORD-123")
    logger.info("Program completed")


# noinspection PyStringConversionWithoutDunderMethod
def configure_logger() -> PythonLoggerAdapter:
    configure_logging()

    uuid_: uuid.UUID = uuid.uuid4()
    correlation_id.set(str(uuid_))

    logger_adapter: PythonLoggerAdapter = PythonLoggerAdapter(__name__)
    return logger_adapter


def main() -> None:
    # Action with start and end record

    # Record start
    start = time.perf_counter()
    logger = configure_logger()

    # your code here
    action(logger)

    # record end
    end = time.perf_counter()

    logger.info(f"Execution time: {end - start:.6f} seconds")


if __name__ == "__main__":
    main()
