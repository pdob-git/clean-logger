import atexit
import logging
from logging.handlers import QueueListener
from logging.handlers import RotatingFileHandler

from .config import LOG_QUEUE


_listener: QueueListener | None = None


def start_listener() -> None:
    global _listener

    console = logging.StreamHandler()

    file_handler = RotatingFileHandler(
        "app.log",
        maxBytes=10_000_000,
        backupCount=5
    )

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s "
        "[corr=%(correlation_id)s] "
        "%(name)s %(message)s"
    )

    console.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    _listener = QueueListener(
        LOG_QUEUE,
        console,
        file_handler,
        respect_handler_level=True
    )

    _listener.start()

    atexit.register(stop_listener)


def stop_listener() -> None:
    global _listener
    if _listener:
        _listener.stop()