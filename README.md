# embcli - CLI for Embeddings

[![PyPI](https://img.shields.io/pypi/v/embcli-core?label=PyPI)](https://pypi.org/project/embcli-core/)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mocobeta/embcli/ci.yml?logo=github&label=tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/embcli-core)

## Overview

`embcli` is a command-line interface with a collection of plugins that provide access to various embedding models and vector stores, allowing users to test and compare their performance from the terminal easily. It provides a unified interface for various embedding models, making it easy to generate embeddings, calculate similarity scores, perform document indexing and search, and more!

embcli is designed to be extensible (in a similar way to [llm utility](https://github.com/simonw/llm)), so you can add your own plugins for any embedding model or API you want to use.

## Documentation and Tutorials

- [Quick Start](https://embcli.mocobeta.dev/)
- [Basic Command Usage](https://embcli.mocobeta.dev/#basic_usage/)
- [Vector Search Usage](https://embcli.mocobeta.dev/#vector_search/)

## Project Status

Pre-alpha. embcli is in active development, and new features and plugins are being added regularly.

## Supported Models

embcli supports a variety of embedding models, both proprietary and open source. Each model is provided as a plugin, which can be installed separately. The `emb` command provides a unified interface for all models.

See [Model Plugins](https://embcli.mocobeta.dev/#model_plugins/) for the full list of available models.

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

## Build documentation

```bash
uv run mkdocs build -f docs/mkdocs.yml
```

## How is this different from llm command-line tool?

This tool is greatly influenced by llm, but its purpose is slightly different. While the llm command can handle embeddings, its main focus may not on embeddings (representation models) but on large language models. My motivation for creating this tool is to provide a feature-rich command-line utility for embeddings, for building semantic search, RAG applications, and other downstream tasks.

## License

Apache License 2.0
