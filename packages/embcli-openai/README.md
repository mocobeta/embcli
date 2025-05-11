# embcli-openai

openai plugin for embcli, a command-line interface for embeddings.

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

You need to have an OpenAI API key to run the tests for the `embcli-openai` package. You can set it up as an environment variable:

```bash
OPENAI_API_KEY=<YOUR_OPENAI_KEY> RUN_OPENAI_TESTS=1 uv run --package embcli-openai pytest packages/embcli-openai/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-openai
uv run ruff format packages/embcli-openai
```

### Run Type Checker

```bash
uv run --package embcli-openai pyright packages/embcli-openai
```

## Build

```bash
uv build --package embcli-openai
```

## License

Apache License 2.0
