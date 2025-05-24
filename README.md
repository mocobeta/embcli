# embcli - CLI for Embeddings

[![PyPI](https://img.shields.io/pypi/v/embcli-core?label=PyPI)](https://pypi.org/project/embcli-core/)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mocobeta/embcli/ci.yml?logo=github&label=tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/embcli-core)
![PyPI - License](https://img.shields.io/pypi/l/embcli-core)

## Overview

`embcli` is a command-line interface with a collection of plugins that provide access to various embedding models and vector stores, allowing users to test and compare their performance from the terminal easily. It provides a unified interface for various embedding models, making it easy to generate embeddings, calculate similarity scores, perform document indexing and search, and more!

embcli is designed to be extensible (in a similar way to [llm utility](https://github.com/simonw/llm)), so you can add your own plugins for any embedding model or API you want to use.

## Project Status

Pre-alpha. embcli is in active development, and new features and plugins are being added regularly.

## Usage

`emb --help` shows the basic usage of the command-line tool.

```bash
emb --help
Usage: emb [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  collections        List collections in the vector store.
  delete-collection  Delete a collection from the vector store.
  embed              Generate embeddings for the provided text or file...
  ingest             Ingest documents into the vector store.
  ingest-sample      Ingest example documents into the vector store.
  models             List available models.
  search             Search for documents in the vector store for the query.
  simscore           Calculate similarity score between two texts.
  vector-stores      List available vector stores.
```

See README of each package (plugin) for usage instructions for specific models.

### Proprietary Models

- [embcli-openai](packages/embcli-openai/README.md)
- [embcli-cohere](packages/embcli-cohere/README.md)
- [embcli-gemini](packages/embcli-gemini/README.md)
- [embcli-jina](packages/embcli-jina/README.md)
- [embcli-mistral](packages/embcli-mistral/README.md)
- [embcli-voyage](packages/embcli-voyage/README.md)

### Open Source Models

- [embcli-sbert](packages/embcli-sbert/README.md)
- [embcli-llamacpp](packages/embcli-llamacpp/README.md)

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

## How is this different from llm command-line tool?

This tool is greatly influenced by llm, but its purpose is slightly different. While the llm command can handle embeddings, its main focus may not on embeddings (representation models) but on large language models. My motivation for creating this tool is to provide a feature-rich command-line utility for embeddings, for building semantic search, RAG applications, and other downstream tasks.

## License

Apache License 2.0
