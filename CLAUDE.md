# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Build
```bash
# Build all packages
uv build --all-packages

# Build specific package
uv build --package embcli-core
```

### Run Tests
```bash
# Run tests for specific package
uv run --package embcli-core pytest packages/embcli-core/tests

# Run a single test
uv run --package embcli-core pytest packages/embcli-core/tests/embcli_core/test_cli_embed.py::test_function_name
```

### Linting and Formatting
```bash
# Run linter and formatter on all packages
uv run ruff check --fix
uv run ruff format

# Run on specific package
uv run ruff check --fix packages/embcli-core
uv run ruff format packages/embcli-core
```

### Type Checking
```bash
# Run type checker for specific package
uv run --package embcli-core pyright packages/embcli-core
```

### Documentation
```bash
# Build documentation
uv run mkdocs build -f docs/mkdocs.yml
```

## High-Level Architecture

embcli is a plugin-based CLI for working with embedding models and vector stores. The architecture follows these key principles:

### Core Components

1. **embcli-core**: The main package containing:
   - CLI interface (`cli.py`) - Command-line interface using Click
   - Plugin system (`plugins.py`) - Uses pluggy for plugin management
   - Base classes (`models.py`, `vector_stores.py`) - Abstract base classes for embedding models and vector stores
   - Document handling (`document.py`, `document_loader.py`) - Document types and loading utilities

2. **Plugin Architecture**:
   - Each embedding model is a separate package (e.g., `embcli-openai`, `embcli-gemini`)
   - Models register themselves via setuptools entry points
   - Plugin discovery happens through `pluggy.PluginManager`
   - Hooks are defined in `hookspecs.py`

3. **Model Types**:
   - `EmbeddingModel`: Base class for text embedding models
   - `MultimodalEmbeddingModel`: Extends EmbeddingModel for image support
   - `LocalEmbeddingModel`: For models that run locally (e.g., sentence-transformers)

4. **Vector Store Integration**:
   - Abstract `VectorStore` base class defines interface
   - Currently supports LanceDB via `vector_store/lancedb.py` as default implementation
   - Vector stores handle document ingestion and similarity search

### Key Design Patterns

- **Plugin Registration**: Models and vector stores register via `embedding_model()` and `vector_store()` hooks
- **Batch Processing**: All models support batch embedding generation for efficiency
- **Model Aliases**: Each model can have multiple aliases for user convenience
- **Environment Variables**: API keys and configuration loaded from `.env` files
- **Separation of Concerns**: Core functionality separate from vendor-specific implementations

### Adding New Models

To add a new embedding model:
1. Create a new package under `packages/embcli-<vendor>`
2. Implement the `EmbeddingModel` or `MultimodalEmbeddingModel` interface
3. Register the model via setuptools entry point in `pyproject.toml`
4. Add appropriate tests following the existing pattern