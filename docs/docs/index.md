# embcli - CLI for Embeddings

embcli is a command-line interface for embeddings. It provides a unified interface for various embedding models, making it easy to generate embeddings, calculate similarity scores, perform document indexing and search, and more!

## Quick start

### Installation

Install `embcli-sbert` plugin to use sentence-transformers models.

```bash
pip install embcli-sbert
```

[Model Plugins](model_plugins.md) shows the full list of available model plugins.

### emb command

A plugin contains `emb` command, which provides a unified interface for embedding models. `--help` option shows the general usage of `emb` command.

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

### Try out the Embedding Models

Get an embedding for an input text by a sentence-transformers model (all-MiniLM-L6-v2).

```bash
emb embed -m sbert/all-MiniLM-L6-v2 \
"Owls can rotate their necks 270 degrees without injury🦉"
```

Calculate similarity score between two text embeddings by all-MiniLM-L6-v2. The default metric is cosine similarity.

```bash
emb simscore -m sbert/all-MiniLM-L6-v2 \
"The cat drifts toward sleep." "Sleep dances in the cat's eyes."
```

Index a sample corpus in a Chroma vector store collection. The default database path is `./chroma.db`.

```bash
emb ingest-sample -m sbert/all-MiniLM-L6-v2 -c catcafe --corpus cat-names-en
```

Search documents for a query in the indexed Chroma collection.

```bash
emb search -m sbert/all-MiniLM-L6-v2 -c catcafe -q "Who's the most agile?"
```