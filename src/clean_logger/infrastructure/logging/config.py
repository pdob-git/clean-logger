import logging

from .context_formatter import ContextFormatter


class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        from .context import correlation_id

        record.correlation_id = correlation_id.get()
        return True


def configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(
        ContextFormatter("%(asctime)s %(levelname)s [run=%(correlation_id)s] %(name)s %(message)s")
    )
    handler.addFilter(CorrelationIdFilter())

    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(logging.INFO)
