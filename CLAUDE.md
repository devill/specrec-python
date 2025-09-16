# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Testing
- Install in development mode: `pip install -e .[test,dev]`
- Run tests: `pytest`
- Run tests with coverage: `pytest --cov=src/specrec --cov-report=html`
- Run specific test: `pytest tests/test_module.py::test_function`

### Code Quality
- Format code: `black .`
- Type checking: `mypy .`
- Lint code: `flake8`
- Run pre-commit hooks: `pre-commit run --all-files`

### Build
- Build package: `python -m build`
- Clean build artifacts: `rm -rf dist/ build/ *.egg-info/`

## Architecture Overview

This is the Python implementation of SpecRec, a legacy testing library that enables testing untestable code through record-replay.

### Key Components

**ObjectFactory** - Dependency injection replacement for direct instantiation
- Singleton pattern for controlling object creation in tests
- `create<T>(constructor_args)` method for testable dependencies
- Global convenience functions for easy integration

**Context** - High-level test orchestration API
- Primary entry point via `Context.verify()`
- Fluent API for test double configuration
- Automatic test isolation and cleanup

**CallLogger** - Records method interactions
- Uses Python's dynamic nature for transparent method interception
- Outputs human-readable specifications with emoji decorations
- Thread-safe logging with context management

**Parrot** - Replays interactions from verified files
- Reads `.verified.txt` files for predetermined return values
- Uses dynamic proxy creation for method call matching
- Eliminates manual mock setup requirements

### Testing Framework Integration

- Built for pytest testing framework
- Uses approvaltests for approval-style testing
- Supports `.received.txt`/`.verified.txt` workflow
- Data-driven testing from verified specification files

### Python-Specific Features

- Python 3.8+ compatibility
- Type hints throughout codebase
- Uses dataclasses and modern Python patterns
- Integration with Python's unittest.mock where appropriate

### Important Notes

- Requires Python 3.8+
- Uses hatchling build backend
- Black code formatting (88 char line length)
- mypy strict type checking enabled