# embcli-jina

jina plugin for embcli, a command-line interface for embeddings.

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

You need to have a Jina API key to run the tests for the `embcli-jina` package. You can set it up as an environment variable:

```bash
JINA_API_KEY=<YOUR_JINA_KEY> RUN_JINA_TESTS=1 uv run --package embcli-jina pytest packages/embcli-jina/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-jina
uv run ruff format packages/embcli-jina
```

### Run Type Checker

```bash
uv run --package embcli-jina pyright packages/embcli-jina
```

## Build

```bash
uv build --package embcli-jina
```

## License

Apache License 2.0
