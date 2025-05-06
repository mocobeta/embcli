# embcli - CLI for Embeddings

## Development

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv)

### Setup

```bash
git clone https://github.com/mocobeta/embcli.git
cd embcli
uv venv
```

### Run Tests

For `embcli-core` package:

```bash
uv run --package embcli-core pytest packages/embcli-core/tests
```

For `embcli-openai` package:

```bash
OPENAI_API_KEY=<YOUR_OPENAI_KEY> RUN_OPENAI_TESTS=1 uv run --package embcli-openai pytest packages/embcli-openai/tests/
```
### Run Linter and Formatter

```bash
uv run ruff check --fix
uv run ruff format
```

### Pre-commit Hooks to Run Linter and Formatter (optional)

If you want to run the ruff linter and formatter in pre-commit hooks, you need to set up the pre-commit hook manually.

```bash
uv run pre-commit install
vim .git/hooks/pre-commit
# Edit the pre-commit hook to use 'uv run' instead of directly running pre-commit
    # exec pre-commit "${ARGS[@]}"
    exec uv run pre-commit "${ARGS[@]}"
```

See [pre-commit](https://pre-commit.com/) for more information.

### Run Type Checker

```bash
uv run --package embcli-core pyright packages/embcli-core
```

## Build

```bash
uv build --all-packages
```