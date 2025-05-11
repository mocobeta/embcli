# embcli-mistral

mistral plugin for embcli, a command-line interface for embeddings.

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

You need to have a Mistral API key to run the tests for the `embcli-mistral` package. You can set it up as an environment variable:

```bash
MISTRAL_API_KEY=<YOUR_MISTRAL_KEY> RUN_MISTRAL_TESTS=1 uv run --package embcli-mistral pytest packages/embcli-mistral/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-mistral
uv run ruff format packages/embcli-mistral
```

### Run Type Checker

```bash
uv run --package embcli-mistral pyright packages/embcli-mistral
```

## Build

```bash
uv build --package embcli-mistral
```

## License

Apache License 2.0
