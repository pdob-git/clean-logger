# AGENTS.md

## 📄 Overview

This repository follows a **Clean Architecture** style for a small logging demo.  The following sections provide command‑line shortcuts and style guidelines that agents (and humans) can use as a reference.

---

## 🔧 Build / Test / Lint

All tasks are executed from the repository root (`E:\p525959_data\Projects\Python\opencode\clean-logger`).

| Command | Description |
|---------|-------------|
| `pip install -e .` | Install the package in editable mode along with development dependencies.
| `pytest` | Run the entire test suite.
| `pytest <test_file>::<test_name>` | Run a single test (e.g. `pytest tests/test_fakes.py::test_logs_order_created`).
| `ruff check . --fix` | Run the RUF linter and auto‑apply quick fixes.
| `ruff format .` | Apply project‑wide formatting according to the Ruff config.
| `mypy src/clean_logger` | Type‑check the application code.
| `pre-commit run --all-files` | Run the full pre‑commit hook set (ruff, mypy, etc.) on all files.
|
> **Tip**: To preview a single test’s console output without the full test harness, use
> ```bash
> python -m unittest tests.test_fakes.TestClass.test_name -v
> ````.

---

## 📑 Code‑Style Guidelines

* **Imports** – All imports should follow PEP‑8 ordering: standard library, typing, third‑party, local modules.  Use absolute imports; avoid `from .module import …` inside packages.
* **Formatting** – Ruff handles formatting; aim for 4‑space indentation, no trailing whitespace, and a maximum line length of 88 characters.
* **Type hints** – Every public function or class should include type annotations.  Use `Protocol` for interfaces, `Callable[[str], AppLogger]` for logger factories.
* **Naming** –
  * Modules: snake_case.
  * Classes / protocols: PascalCase.
  * Functions / methods / variables: snake_case.
  * Constants: UPPER_SNAKE.
* **Error handling** – Catch only known exceptional conditions; re‑raise or log wrapped exceptions.
* **Logging** – Do NOT import the stdlib `logging` in the `application` layer.  Use the `AppLogger` port.  All messages should include context via keyword arguments so the log formatter can serialize them.
* **Documentation** – Module docstrings should explain the module’s purpose.  Public functions/classes must have a short docstring after the `def …` line.
* **Tests** – Each test file lives under `tests/`.  Use `pytest` fixtures for common setups.  Keep tests deterministic – avoid network or file system side effects.

---

## ✂️ Cursor Rules (if any)

No custom Cursor rules were found.  If you need to create them, add JSON files under `.cursor/rules/` following the [Cursor documentation](https://github.com/yourorganization/cursor).

---

## 🤖 Copilot‑Instructions (if any)

No `.github/copilot-instructions.md` was present.  If you wish to provide Copilot prompts, create a file in that name with markdown prompts.

---

## 📦 Project Structure Recap

```
src/clean_logger/
├── __init__.py
├── py.typed
├── application/
│   ├── __init__.py
│   ├── ports/
│   │   ├── __init__.py
│   │   └── logger.py
│   └── use_cases/
│       ├── __init__.py
│       └── create_order.py
├── infrastructure/
│   ├── __init__.py
│   └── logging/
│       ├── __init__.py
│       ├── adapters.py
│       ├── config.py
│       ├── context.py
│       ├── listener.py
│       └── ...
└── presentation/
    ├── __init__.py
    └── cli.py
```

---

## 🔍 Quick Reference for Agents

| Area | Key Files | Common Tasks |
|------|-----------|--------------|
| **Use‑cases** | `src/clean_logger/application/use_cases/create_order.py` | Instantiate with `CreateOrderUseCase(PythonLoggerAdapter)` and call `.execute(order_id)` |
| **Logging** | `src/clean_logger/infrastructure/logging/adapters.py` | Implement or mock `AppLogger` for tests |
| **CLI** | `src/clean_logger/presentation/cli.py` | Run with `python -m clean_logger` or `python src/clean_logger/presentation/cli.py` |
| **Testing** | `tests/test_fakes.py` | Verify logger interactions |

---

All the commands above are meant to be used by agentic tools or humans.  Feel free to tweak the `AGENTS.md` as the repository evolves.
