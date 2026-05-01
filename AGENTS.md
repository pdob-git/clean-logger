# AGENTS.md

## Overview

This repository demonstrates **Clean Architecture** with a logging implementation. The codebase serves as a reference for building Python applications with clear separation between domain, application, infrastructure, and presentation layers.

---

## Build / Test / Lint Commands

All tasks run from the repository root (`/home/synkmint/Gitrepos/Python/opencode/clean-logger`).

| Command | Description |
|---------|-------------|
| `pip install -e .` | Install package in editable mode with dev dependencies |
| `pip install -e ".[dev]"` | Install with all development tools (mypy, pytest, etc.) |
| `pytest` | Run entire test suite |
| `pytest tests/test_fakes.py::test_logs_order_created` | Run a single test by name |
| `python -m unittest tests.test_fakes.test_logs_order_created -v` | Run single test with verbose output |
| `ruff check . --fix` | Run linter and auto-apply fixes |
| `ruff format .` | Apply project-wide formatting |
| `mypy src/clean_logger` | Type-check application code |
| `mypy src/clean_logger --strict` | Strict type checking |
| `pre-commit run --all-files` | Run full pre-commit hook set |
| `python -m clean_logger` | Run the CLI application |

---

## Code Style Guidelines

### Imports

- Follow PEP-8 ordering: standard library → typing → third-party → local modules
- Use absolute imports (e.g., `from clean_logger.application.ports.logger import AppLogger`)
- Avoid relative imports (`from .module import ...`) inside packages
- Group imports with blank lines between categories

### Formatting (Ruff)

- 4-space indentation, no tabs
- No trailing whitespace
- Maximum line length: 100 characters (configured in pyproject.toml)
- Ruff handles all formatting automatically

### Type Hints

- Every public function/class must have type annotations
- Use `Protocol` for interfaces (see `application/ports/logger.py`)
- Use `Callable[[str], AppLogger]` for factory types
- Enable strict mode with `--strict` for new code

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | snake_case | `create_order.py` |
| Classes/Protocols | PascalCase | `AppLogger`, `CreateOrderUseCase` |
| Functions/Methods | snake_case | `execute()`, `configure_logging()` |
| Variables | snake_case | `logger`, `order_id` |
| Constants | UPPER_SNAKE | `LOG_QUEUE`, `DEFAULT_TIMEOUT` |

### Error Handling

- Catch only known exceptional conditions
- Re-raise or log wrapped exceptions
- Avoid catching `Exception` or `BaseException` indiscriminately
- Use specific exception types

### Logging Rules

- **NEVER** import stdlib `logging` in the `application` layer
- Use the `AppLogger` port interface instead
- Pass context via keyword arguments: `logger.info("Order created", order_id=order_id)`
- Avoid string interpolation in log messages

### Documentation

- Module docstrings: explain the module's purpose (1-2 sentences)
- Public classes/functions: short docstring after the `def`/`class` line
- Use Google-style docstrings for complex functions

---

## Architecture Layers

```
src/clean_logger/
├── domain/           # Business entities (no dependencies)
│   └── entities/     # Order, etc.
├── application/     # Use cases and ports (depends only on domain)
│   ├── ports/        # Interfaces (AppLogger Protocol)
│   └── use_cases/    # Business logic (CreateOrderUseCase)
├── infrastructure/  # External concerns (depends on application)
│   └── logging/     # Logger adapters, config, context
└── presentation/     # UI/CLI (depends on application)
    └── cli.py       # Entry point
```

---

## Quick Reference

| Area | Key Files | Usage |
|------|-----------|-------|
| **Logger Interface** | `application/ports/logger.py` | Protocol defining `AppLogger` |
| **Logger Implementation** | `infrastructure/logging/adapters.py` | `PythonLoggerAdapter` concrete impl |
| **Logging Config** | `infrastructure/logging/config.py` | `configure_logging()` sets up handlers |
| **Correlation ID** | `infrastructure/logging/context.py` | `correlation_id` ContextVar |
| **Use Case** | `application/use_cases/create_order.py` | `CreateOrderUseCase` example |
| **CLI Entry** | `presentation/cli.py` | Main function, run with `-m clean_logger` |
| **Tests** | `tests/test_fakes.py` | FakeLoggerAdapter for testing |

---

## Testing Guidelines

- Place tests under `tests/` directory
- Test files must be named `test_*.py`
- Use `FakeLoggerAdapter` (extends `PythonLoggerAdapter`) to capture log messages
- Keep tests deterministic: avoid network calls, file system I/O
- Use pytest fixtures for common setup

---

## Development Workflow

1. **Create a branch**: `git checkout -b feature/your-feature`
2. **Make changes** following code style guidelines
3. **Run tests**: `pytest`
4. **Run type checks**: `mypy src/clean_logger`
5. **Run linter**: `ruff check . --fix && ruff format .`
6. **Commit**: `git add . && git commit -m "description"`
7. **Push**: `git push -u origin your-branch`

---

## Dependencies

- Python 3.12+
- `truststore` - Secure certificate handling
- `logging` - Standard library logging (infrastructure layer only)

Dev dependencies: `pytest`, `mypy`, `ruff`, `pre-commit`

---

## Common Patterns

### Adding a New Use Case

```python
# src/clean_logger/application/use_cases/new_use_case.py
from typing import Callable
from clean_logger.application.ports.logger import AppLogger

LoggerProvider = Callable[[str], AppLogger]

class NewUseCase:
    def __init__(self, logger_provider: LoggerProvider) -> None:
        self._logger = logger_provider(__name__)

    def execute(self, data: str) -> None:
        self._logger.info("Action started", data=data)
        # business logic
        self._logger.info("Action completed", data=data)
```

### Adding a New Logger Adapter

```python
# src/clean_logger/infrastructure/logging/new_adapter.py
from typing import Any
from clean_logger.application.ports.logger import AppLogger

class NewLoggerAdapter(AppLogger):
    def __init__(self, name: str) -> None:
        self._name = name

    def debug(self, message: str, **context: Any) -> None: ...
    def info(self, message: str, **context: Any) -> None: ...
    def warning(self, message: str, **context: Any) -> None: ...
    def error(self, message: str, **context: Any) -> None: ...
```

---

For questions or improvements, open an issue or submit a PR.