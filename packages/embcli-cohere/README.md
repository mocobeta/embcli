# embcli-cohere

cohere plugin for embcli, a command-line interface for embeddings.

## Reference

- [Cohere’s Embed Models](https://docs.cohere.com/v2/docs/cohere-embed)

## Installation

```bash
pip install embcli-cohere
```

## Quick Start

You need Cohere API key to use this plugin. Set `COHERE_API_KEY` environment variable in `.env` file in the current directory. Or you can give the env file path by `-e` option.

```bash
cat .env
COHERE_API_KEY=<YOUR_COHERE_KEY>
```

### Try out the Embedding Models

```bash
# show general usage of emb command.
emb --help

# list all available models.
emb models
CohereEmbeddingModel
    Vendor: cohere
    Models:
    * embed-v4.0 (aliases: embed-v4)
    * embed-english-v3.0 (aliases: embed-en-v3)
    * embed-english-light-v3.0 (aliases: embed-en-light-v3)
    * embed-multilingual-v3.0 (aliases: embed-multiling-v3)
    * embed-multilingual-light-v3.0 (aliases: embed-multiling-light-v3)
    Model Options:
    * input_type (str) - The type of input, affecting how the model processes it. Options include 'search_document', 'search_query', 'classification', 'clustering', 'image'.
    * truncate (str) - How to handle text inputs that exceed the model's token limit. Options include 'none', 'start', 'end', 'middle'.

# get an embedding for an input text by embed-v4.0 model.
emb embed -m embed-v4 "Embeddings are essential for semantic search and RAG apps."

# get an embedding for an input text by embed-v4.0 model with input_type=search_query.
emb embed -m embed-v4 "Embeddings are essential for semantic search and RAG apps." -o input_type search_query

# calculate similarity score between two texts by embed-v4.0 model. the default metric is cosine similarity.
emb simscore -m embed-v4 "The cat drifts toward sleep." "Sleep dances in the cat's eyes."
0.6656540804655765
```

### Document Indexing and Search

You can use the `emb` command to index documents and perform semantic search. `emb` uses [`chroma`](https://github.com/chroma-core/chroma) for the default vector database.

```bash
# index example documents in the current directory.
emb ingest-sample -m embed-v4 -c catcafe --corpus cat-names

# or, you can give the path to your documents.
# the documents should be in a CSV file with two columns: id and text. the separator should be comma.
emb ingest -m embed-v4 -c catcafe -f <path-to-your-documents>

# search for a query in the indexed documents.
emb search -m embed-v4 -c catcafe -q "Who's the naughtiest one?"
Found 5 results:
Score: 0.4193700736149105, Document ID: 97, Text: Alfie: Alfie is a cheerful and mischievous little cat, always getting into playful trouble with a charming innocence. He loves exploring small spaces and batting at dangling objects. Alfie is incredibly affectionate, quick to purr and eager for cuddles, a delightful bundle of joy and entertainment for his humans.
Score: 0.4187830451687781, Document ID: 76, Text: Frankie: Frankie is a boisterous and playful cat, full of charm and mischief. He loves to zoom around the house and engage in energetic play sessions, especially with crinkly toys. Frankie is also very affectionate, often seeking out his humans for cuddles and purrs after his bursts of energy, a fun-loving friend.
Score: 0.41594965013771756, Document ID: 46, Text: Bandit: Bandit is a mischievous cat, often with mask-like markings, always on the lookout for his next playful heist of a toy or treat. He is clever and energetic, loving to chase and pounce. Despite his roguish name, Bandit is a loving companion who enjoys a good cuddle after his adventures.
Score: 0.41532520111462273, Document ID: 28, Text: Loki: Loki is a mischievous and clever cat, always finding new ways to entertain himself, sometimes at his humans' expense. He is a master of stealth and surprise attacks on toys. Despite his playful trickery, Loki is incredibly charming and affectionate, easily winning hearts with his roguish appeal.
Score: 0.4081888584294111, Document ID: 50, Text: Dexter: Dexter is a clever and sometimes quirky cat, always up to something interesting. He might have a fascination with running water or a particular toy he carries everywhere. Dexter is highly intelligent and enjoys interactive play, keeping his humans entertained with his unique personality and amusing antics, a truly engaging companion.
```

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

You need to have a Cohere API key to run the tests for the `embcli-cohere` package. You can set it up as an environment variable:

```bash
COHERE_API_KEY=<YOUR_COHERE_KEY> RUN_COHERE_TESTS=1 uv run --package embcli-cohere pytest packages/embcli-cohere/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-cohere
uv run ruff format packages/embcli-cohere
```

### Run Type Checker

```bash
uv run --package embcli-cohere pyright packages/embcli-cohere
```

## Build

```bash
uv build --package embcli-cohere
```

## License

Apache License 2.0
