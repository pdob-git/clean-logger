import logging
from logging.handlers import RotatingFileHandler

from .context_formatter import ContextFormatter


class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        from .context import correlation_id

        record.correlation_id = correlation_id.get()
        return True


def configure_logging() -> None:
    # create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ContextFormatter("%(asctime)s - %(message)s"))
    console_handler.addFilter(CorrelationIdFilter())

    root = logging.getLogger()

    # create file handler which logs more detailed information
    file_handler = RotatingFileHandler("app.log", maxBytes=10_000_000, backupCount=5)

    # create formatter and add it to the file handlers
    file_formatter = ContextFormatter(
        "%(asctime)s %(levelname)s [run=%(correlation_id)s] %(name)s %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # add the handlers to logger
    root.addHandler(console_handler)
    root.addHandler(file_handler)

    root.setLevel(logging.INFO)
