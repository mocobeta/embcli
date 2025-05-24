# embcli - CLI for Embeddings

[![PyPI](https://img.shields.io/pypi/v/embcli-core?label=PyPI)](https://pypi.org/project/embcli-core/)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mocobeta/embcli/ci.yml?logo=github&label=tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/embcli-core)

Core library for embcli, a command-line interface for embeddings.

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

```bash
uv run --package embcli-core pytest packages/embcli-core/tests
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-core
uv run ruff format packages/embcli-core
```

### Run Type Checker

```bash
uv run --package embcli-core pyright packages/embcli-core
```

## Build

```bash
uv build --package embcli-core
```

## License

Apache License 2.0
