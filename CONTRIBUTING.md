# Contributing to Personal Assistant AI

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/WeAreHuman/personal-asistant.git
cd personal-asistant/backend
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
```

## Code Style

- **Black** for formatting (`black .`)
- **isort** for import sorting (`isort . --profile black`)
- **flake8** for linting (`flake8 . --max-line-length=88 --extend-ignore=E203`)
- Max line length: **88** characters

## Running Tests

```bash
cd backend
pytest tests/ -v --cov=app --cov-report=term-missing
```

Tests use an in-memory SQLite database — no external services required.

## Pull Request Guidelines

1. Fork the repository and create a feature branch from `main`.
2. Write tests for new features or bug fixes.
3. Ensure all tests pass and linting is clean before opening a PR.
4. Keep PRs focused — one feature or fix per PR.
5. Update the README if your change affects usage.

## Commit Messages

Use the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
feat: add task priority filtering
fix: correct weather API timeout handling
docs: update API endpoint table
```

## Reporting Issues

Open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs. actual behaviour
- Your environment (Python version, OS)
