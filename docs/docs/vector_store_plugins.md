# Vector Store Plugins

A vector store plugin is a Python package for a specific vector store implementation. All vector store plugins can be used to store and search embeddings via the unified CLI interface.

## [embcli-chroma](https://pypi.org/project/embcli-chroma/) for ChromaDB

The `embcli-chroma` plugin provides ChromaDB integration.

**Installation:** `pip install embcli-chroma`

`emb vector-stores` command shows the available vector stores with their short aliaases.

```bash
emb vector-stores
ChromaVectorStore
    Vendor: chroma
LanceDBVectorStore
    Vendor: lancedb
```

**Example usage:** store and search embeddings in ChromaDB.

We assume you have installed the [embcli-sbert](https://pypi.org/project/embcli-sbert/) plugin to generate embeddings.

```bash
# index example documents to a Chroma collection. Default chroma db path is `./chroma`.
emb ingest-sample -m sbert -c catcafe --corpus cat-names-en --vector-store chroma

# or, you can give the path to your db path.
emb ingest-sample -m sbert -c catcafe --corpus cat-names-en --vector-store chroma --persist-path /path/to/chroma

# search indexed documents in a Chroma collection.
emb search -m sbert -c catcafe -q "Who's the naughtiest one?" --vector-store chroma

# or, you can give the path to your db path.
emb search -m sbert -c catcafe -q "Who's the naughtiest one?" --vector-store chroma --persist-path /path/to/chroma
```


