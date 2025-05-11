# embcli-voyage

voyage plugin for embcli, a command-line interface for embeddings.

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

You need to have a Voyage API key to run the tests for the `embcli-voyage` package. You can set it up as an environment variable:

```bash
VOYAGE_API_KEY=<YOUR_VOYAGE_KEY> RUN_VOYAGE_TESTS=1 uv run --package embcli-voyage pytest packages/embcli-voyage/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-voyage
uv run ruff format packages/embcli-voyage
```

### Run Type Checker

```bash
uv run --package embcli-voyage pyright packages/embcli-voyage
```

## Build

```bash
uv build --package embcli-voyage
```

## License

Apache License 2.0
