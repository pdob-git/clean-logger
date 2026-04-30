# Clean‑logger

> A minimal, **Clean‑Architecture‑style** demo that shows how to wire a flexible logging port into an application.

---

## Introduction

* **Clean‑architecture** keeps the business logic (use‑cases) free from infrastructure concerns such as logging, databases, or networks. 
* The *application* layer only knows about an `AppLogger` protocol.  Concrete implementations live in the *infrastructure* layer.
* This repository contains a tiny demo that:
  * Creates an order via a use‑case.
  * Logs every step using a `PythonLoggerAdapter` that delegates to the standard library `logging` module.
  * Provides a simple CLI that demonstrates the full pipeline.

---

## Architecture

```
┌───────────────────────┐
│  Presentation         │
│  (CLI)                │
└───────┬───────────────┘
        │
┌──┌────▼─────────────────────┐┐
│  | Application (use‑cases)  ││
│  └───┬──────────────────────┘┐
│      │                       │
│  ┌───▼────────┐              │
│  │   Ports    │              │
│  │AppLogger   │              │
│  └─────┬──────┘              │
│        │                     │
│  ┌─────▼────────┐            │
│  │Infrastructure│            │
│  │ (logging,    │            │
│  │ adapters)    │            │
│  └─────┬────────┘            │
│        │                     │
│  ┌─────▼───────┐             │
│  │  Domain     │             │
│  └─────────────┘             │
└──────────────────────────────┘
```

> The diagram is intentionally simple; in a real application the **Domain** and **Infrastructure** sections would be richer.

---

## Installation

```bash
# Install in editable mode with dev dependencies
pip install -e .[dev]
```

> The optional `[dev]` extra pulls in `pytest`, `ruff`, `mypy`, and the `pre‑commit` hooks.

---

## Running the Demo

```bash
# Fast‑track: run the CLI directly via Python module
python -m clean_logger
```

You should see something like:

```
2026-04-30 12:59:51,673 INFO [run=9c324cba-5972-45ba-b99c-451e22196bd7] clean_logger.presentation.cli Program started
2026-04-30 12:59:51,673 INFO [run=9c324cba-5972-45ba-b99c-451e22196bd7] clean_logger.application.use_cases.create_order Creating order | {'order_id': 'ORD-123'}
2026-04-30 12:59:51,673 INFO [run=9c324cba-5972-45ba-b99c-451e22196bd7] clean_logger.application.use_cases.create_order Order created | {'order_id': 'ORD-123'}
2026-04-30 12:59:51,673 INFO [run=9c324cba-5972-45ba-b99c-451e22196bd7] clean_logger.presentation.cli Program completed
```

The output is emitted by the standard‐library `logging` module, but a fully‑fledged JSON formatter can be swapped in by editing ``src/clean_logger/infrastructure/logging/config.py``.

---

## Tests

```bash
# Run everything
pytest

# Run a single test file
pytest tests/test_fakes.py::test_logs_order_created
```

`pytest` automatically discovers tests under the ``tests`` package.

---

## Contributing

1. Fork the repo.
2. Create a feature branch: ``git checkout -b feature/my-cool-feature``.
3. Run linting and tests: ``ruff check . --fix && mypy src/clean_logger && pre-commit run --all-files``.
4. Push your changes and open a pull request.

All commits should follow conventional commit style: ``feat: ...`` |
``fix: ...`` |
``docs: ...``.  See the [pre‑commit](.pre-commit-config.yaml) hooks for the required format.

See [conventional commit cheatsheet](docs/conventional-commits-cheatsheet.md)

---

## License

MIT © 2026 Clean‑logger contributors
