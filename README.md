# embcli - CLI for Embeddings

## Usage

See the README of each package for usage instructions.

- [embcli-core](packages/embcli-core/README.md)
- [embcli-openai](packages/embcli-openai/README.md)
- [embcli-cohere](packages/embcli-cohere/README.md)
- [embcli-gemini](packages/embcli-gemini/README.md)
- [embcli-jina](packages/embcli-jina/README.md)
- [embcli-mistral](packages/embcli-mistral/README.md)
- [embcli-voyage](packages/embcli-voyage/README.md)

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

See the README of each package.

### Run Linter and Formatter (all packages)

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

See the README of each package.

## Build (all packages)

```bash
uv build --all-packages
```

## License

Apache License 2.0
