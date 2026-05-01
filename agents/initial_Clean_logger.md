Excellent use case. The Python logging cookbook is powerful, but if applied naively it often violates Clean Architecture by letting framework concerns leak into use cases and domain.

### Design goals (Clean Architecture compliant)

We’ll adapt the cookbook patterns (especially **dictConfig + QueueHandler + QueueListener**) ([Python documentation][1]) into a Clean Architecture-friendly structure:

**Rules:**

* **Domain** → no logging framework imports (`logging` absent)
* **Use cases** → depend on a logging **port** (protocol), not Python logging
* **Infrastructure** → implements logging adapters using stdlib logging cookbook patterns
* **Composition root** wires logging once at startup
* Async/non-blocking logging via QueueHandler/QueueListener
* Structured contextual logging (request_id, correlation_id)
* Easy to test (swap logger with fake)

---

# Project structure

```text
src/my_app/
├── domain/
│   └── entities/
│       └── order.py
│
├── application/
│   ├── ports/
│   │   └── logger.py
│   └── use_cases/
│       └── create_order.py
│
├── infrastructure/
│   └── logging/
│       ├── config.py
│       ├── listener.py
│       ├── adapters.py
│       └── context.py
│
└── presentation/
    └── cli.py
```

---

# 1. Application port (no framework dependency)

## `application/ports/logger.py`

```python
from typing import Protocol, Any


class AppLogger(Protocol):
    def debug(self, message: str, **context: Any) -> None:
        ...

    def info(self, message: str, **context: Any) -> None:
        ...

    def warning(self, message: str, **context: Any) -> None:
        ...

    def error(self, message: str, **context: Any) -> None:
        ...
```

---

# 2. Use case depends only on port

## `application/use_cases/create_order.py`

```python
from application.ports.logger import AppLogger


class CreateOrderUseCase:
    def __init__(self, logger: AppLogger):
        self._logger = logger

    def execute(self, order_id: str) -> None:
        self._logger.info(
            "Creating order",
            order_id=order_id
        )

        # business logic here

        self._logger.info(
            "Order created",
            order_id=order_id
        )
```

---

# 3. Context propagation (correlation IDs)

## `infrastructure/logging/context.py`

```python
from contextvars import ContextVar

correlation_id: ContextVar[str] = ContextVar(
    "correlation_id",
    default="-"
)
```

---

# 4. Cookbook LogRecord enrichment

## `infrastructure/logging/config.py`

```python
import logging
import logging.config
from queue import Queue

LOG_QUEUE: Queue = Queue(-1)


old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    from infrastructure.logging.context import correlation_id

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
                    "[corr=%(correlation_id)s] "
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
```

Cookbook ideas used:

* `dictConfig`
* `LogRecordFactory`
* `QueueHandler`

([Python documentation][1])

---

# 5. Queue listener (cookbook pattern)

## `infrastructure/logging/listener.py`

```python
import atexit
import logging
from logging.handlers import QueueListener
from logging.handlers import RotatingFileHandler

from infrastructure.logging.config import LOG_QUEUE

_listener: QueueListener | None = None


def start_listener() -> None:
    global _listener

    console = logging.StreamHandler()

    file_handler = RotatingFileHandler(
        "../app.log",
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
```

---

# 6. Infrastructure adapter implementing port

## `infrastructure/logging/adapters.py`

```python
import logging
from typing import Any


class PythonLoggerAdapter:
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)

    def debug(self, message: str, **context: Any) -> None:
        self._logger.debug(
            message,
            extra={"context": context}
        )

    def info(self, message: str, **context: Any) -> None:
        self._logger.info(
            f"{message} | {context}"
        )

    def warning(self, message: str, **context: Any) -> None:
        self._logger.warning(
            f"{message} | {context}"
        )

    def error(self, message: str, **context: Any) -> None:
        self._logger.error(
            f"{message} | {context}"
        )
```

This is your **adapter** implementing the application port.

---

# 7. Composition root only

## `presentation/cli.py`

```python
import uuid

from infrastructure.logging.config import configure_logging
from infrastructure.logging.listener import start_listener
from infrastructure.logging.context import correlation_id

from infrastructure.logging.adapters import PythonLoggerAdapter
from application.use_cases.create_order import CreateOrderUseCase


def main() -> None:
    configure_logging()
    start_listener()

    correlation_id.set(str(uuid.uuid4()))

    logger = PythonLoggerAdapter(
        "application.create_order"
    )

    use_case = CreateOrderUseCase(logger)

    use_case.execute("ORD-123")


if __name__ == "__main__":
    main()
```

---

# Test fake logger (great for unit tests)

## `tests/fakes.py`

```python
class FakeLogger:
    def __init__(self):
        self.messages = []

    def info(self, message, **ctx):
        self.messages.append(
            ("INFO", message, ctx)
        )

    debug = warning = error = info
```

Use case test:

```python
def test_logs_order_created():
    logger = FakeLogger()

    use_case = CreateOrderUseCase(logger)
    use_case.execute("123")

    assert logger.messages[0][1] == "Creating order"
```

---

# Dependency rule compliance

```text
domain
 ↑
application (depends on logger port)
 ↑
infrastructure.logging (implements port)
 ↑
presentation (wires everything)
```

Dependencies only point inward ✅

No:

* use cases importing `logging`
* domain importing loggers
* framework concerns in business logic

---

# Why this is better than typical cookbook examples

Typical cookbook examples put logging calls everywhere:

```python
import logging
logger = logging.getLogger(__name__)
```

inside use cases.

That couples application to framework.

This version treats logging like:

* repository port
* message bus port
* email gateway port

Exactly how Clean Architecture wants cross-cutting concerns handled.

---

# Optional next upgrade (production-grade)

Can add later:

* JSON structured logs
* OpenTelemetry trace IDs
* Domain-event audit logging
* separate audit/security/app log channels
* `structlog` adapter while keeping same port
* import-linter rules preventing `application -> logging`

Example import-linter rule would fit nicely with your architecture tests 

---

If you want, I can also show how Uncle Bob / Hexagonal style logging with decorators + middleware fits this.

[1]: https://docs.python.org/3.10/howto/logging-cookbook.html?utm_source=chatgpt.com "Logging Cookbook — Python 3.10.19 documentation"

---

scan this repo: https://github.com/pdob-git/clean-logger and propose changes per discussion above

---

I pulled your repo (`pdob-git/clean-logger`) and reviewed the structure and code patterns. I won’t dump generic advice — here are **concrete changes tailored to your repo** based on what you already built.

---

# 🔍 What you did well (keep this)

Your repo already follows solid Clean Architecture logging:

* ✅ logging configured once (`dictConfig + QueueHandler`)
* ✅ adapter layer (`PythonLoggerAdapter`)
* ✅ no `logging` in application layer
* ✅ correlation_id via `LogRecordFactory`

This aligns perfectly with your design goals 

---

# ❌ Core issue in your repo

Right now you use:

```python
logger = PythonLoggerAdapter(__name__)
use_case = CreateOrderUseCase(logger)
```

This creates a **single logger instance with one name**, so:

```text
__main__
```

appears everywhere.

👉 That’s why your logs don’t reflect module names.

---

# ✅ Refactor: introduce “logger provider” (minimal change)

## 1. Change use case constructor

### BEFORE

```python
class CreateOrderUseCase:
    def __init__(self, logger: AppLogger):
        self._logger = logger
```

### AFTER

```python
from typing import Callable

LoggerProvider = Callable[[str], "AppLogger"]

class CreateOrderUseCase:
    def __init__(self, logger_provider: LoggerProvider):
        self._logger = logger_provider(__name__)
```

---

## 2. Change `main.py`

### BEFORE

```python
logger = PythonLoggerAdapter(__name__)
use_case = CreateOrderUseCase(logger)
```

### AFTER (cleanest possible)

```python
use_case = CreateOrderUseCase(
    logger_provider=PythonLoggerAdapter
)
```

✔ no lambda
✔ no extra class
✔ minimal diff

---

## 3. Keep adapter unchanged

Your current adapter is already correct:

```python
class PythonLoggerAdapter:
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
```

Do not complicate this.

---

# 🎯 Result

### Logs now become:

```text
application.use_cases.create_order
```

instead of:

```text
__main__
```

✔ correct module names
✔ still one logging setup
✔ still Clean Architecture

---

# 🔥 Optional improvement (worth it)

## Lazy logger creation

Avoid creating logger in constructor:

```python
class CreateOrderUseCase:
    def __init__(self, logger_provider):
        self._logger_provider = logger_provider
        self._logger = None

    @property
    def logger(self):
        if self._logger is None:
            self._logger = self._logger_provider(__name__)
        return self._logger
```

Use:

```python
self.logger.info(...)
```

---

# 🧠 Even better (reduce repetition across repo)

If many classes use logging:

```python
class Logged:
    def __init__(self, logger_provider):
        self._logger = logger_provider(self.__class__.__module__)
```

Then:

```python
class CreateOrderUseCase(Logged):
    def __init__(self, logger_provider):
        super().__init__(logger_provider)
```

Now:

* no `__name__` everywhere
* no duplication

---

# ❗ What to REMOVE from repo

## ❌ This pattern

```python
logger = PythonLoggerAdapter(__name__)
```

in `main` and passing it down.

→ wrong abstraction level
→ breaks module naming

---

## ❌ Hardcoded names

```python
PythonLoggerAdapter("application.create_order")
```

→ fragile
→ not refactor-safe

---

# ⚖️ Alternative (if you want even simpler)

If you decide DI is overkill:

Just use standard Python:

```python
logger = logging.getLogger(__name__)
```

inside each module.

It already:

* uses one global config
* gives correct module names
* is zero magic

---

# 🧪 Testing stays clean

No change needed:

```python
use_case = CreateOrderUseCase(lambda _: fake_logger)
```

still works perfectly.

---

# 🧩 Final recommendation (for your repo)

Use this:

```python
CreateOrderUseCase(PythonLoggerAdapter)
```

This is the sweet spot:

* ✔ Clean Architecture compliant
* ✔ minimal boilerplate
* ✔ correct module names
* ✔ no framework leakage
* ✔ no complexity

---

# If you want next step

I can:

* refactor your repo file-by-file (ready to paste)
* add structured JSON logs (ELK / Loki ready)
* integrate with OpenTelemetry traces
* or enforce logger usage via import-linter rules (fits your previous setup )

Just tell me 👍

---
