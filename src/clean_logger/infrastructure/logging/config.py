import logging
import logging.config
from queue import Queue

LOG_QUEUE: Queue = Queue(-1)


old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    from .context import correlation_id

    record = old_factory(*args, **kwargs)
    record.correlation_id = correlation_id.get()
    return record


def configure_logging() -> None:
    logging.setLogRecordFactory(record_factory)

    config = {
        "version": 1,
        "disable_existing_loggers": False,

        "formatters": {
            "standard": {
                "format": (
                    "%(asctime)s "
                    "%(levelname)s "
                    "[run=%(correlation_id)s] "
                    "%(name)s "
                    "%(message)s"
                )
            }
        },

        "handlers": {
            "queue": {
                "class": "logging.handlers.QueueHandler",
                "queue": LOG_QUEUE
            }
        },

        "root": {
            "handlers": ["queue"],
            "level": "INFO"
        }
    }

    logging.config.dictConfig(config)