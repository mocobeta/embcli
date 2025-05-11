# embcli - CLI for Embeddings

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
