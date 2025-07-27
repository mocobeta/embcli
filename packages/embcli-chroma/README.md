# embcli-chroma

[![PyPI](https://img.shields.io/pypi/v/embcli-chroma?label=PyPI)](https://pypi.org/project/embcli-chroma/)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mocobeta/embcli/ci-chroma.yml?logo=github&label=tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/embcli-chroma)

chroma plugin for embcli, a command-line interface for embeddings.

## Reference

- [Chroma](https://www.trychroma.com/)

## Installation

```bash
pip install embcli-chroma
```

## Quick Start

### Use Chroma as a Vector Database

```bash
# show general usage of emb command.
emb --help

# list all available vector stores.
emb vector-stores
ChromaVectorStore
    Vendor: chroma

# index example documents to a Chroma collection. Default chroma db path is `./chroma`.
emb ingest-sample -m sbert -c catcafe --corpus cat-names-en --vector-store chroma

# or, you can give the path to your db path.
emb ingest-sample -m sbert -c catcafe --corpus cat-names-en --vector-store chroma --persist-path /path/to/chroma

# search indexed documents in a Chroma collection.
emb search -m sbert -c catcafe -q "Who's the naughtiest one?" --vector-store chroma

# or, you can give the path to your db path.
emb search -m sbert -c catcafe -q "Who's the naughtiest one?" --vector-store chroma --persist-path /path/to/chroma
```

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

```bash
uv run --package embcli-chroma pytest packages/embcli-chroma/tests
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-chroma
uv run ruff format packages/embcli-chroma
```

### Run Type Checker

```bash
uv run --package embcli-chroma pyright packages/embcli-chroma
```

## Build

```bash
uv build --package embcli-chroma
```

## License

Apache License 2.0
