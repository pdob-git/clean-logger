import logging


class ContextFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)

        context = getattr(record, "context", None)
        if context:
            msg = f"{msg} | {context}"

        return msg
