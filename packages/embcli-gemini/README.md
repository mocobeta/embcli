# embcli-gemini

gemini plugin for embcli, a command-line interface for embeddings.

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

You need to have a Gemini API key to run the tests for the `embcli-gemini` package. You can set it up as an environment variable:

```bash
GEMINI_API_KEY=<YOUR_GEMINI_KEY> RUN_GEMINI_TESTS=1 uv run --package embcli-gemini pytest packages/embcli-gemini/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-gemini
uv run ruff format packages/embcli-gemini
```

### Run Type Checker

```bash
uv run --package embcli-gemini pyright packages/embcli-gemini
```

## Build

```bash
uv build --package embcli-gemini
```

## License

Apache License 2.0
