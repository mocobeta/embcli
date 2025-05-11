# embcli-cohere

cohere plugin for embcli, a command-line interface for embeddings.

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

You need to have a Cohere API key to run the tests for the `embcli-cohere` package. You can set it up as an environment variable:

```bash
COHERE_API_KEY=<YOUR_COHERE_KEY> RUN_COHERE_TESTS=1 uv run --package embcli-cohere pytest packages/embcli-cohere/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-cohere
uv run ruff format packages/embcli-cohere
```

### Run Type Checker

```bash
uv run --package embcli-cohere pyright packages/embcli-cohere
```

## Build

```bash
uv build --package embcli-cohere
```

## License

Apache License 2.0
