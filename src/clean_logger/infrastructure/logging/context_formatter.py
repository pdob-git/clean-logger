import logging

class ContextFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)

        context = getattr(record, "context", None)
        if context:
            msg = f"{msg} | {context}"

        return msg