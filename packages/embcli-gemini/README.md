# embcli-gemini

gemini plugin for embcli, a command-line interface for embeddings.

## Reference

- [Gemini Embedding Experimental](https://ai.google.dev/gemini-api/docs/models#gemini-embedding)
- [Gemini Text Embedding and Embedding](https://ai.google.dev/gemini-api/docs/models#text-embedding)

## Installation

```bash
pip install embcli-gemini
```

## Quick Start

You need Gemini API key to use this plugin. Set `GEMINI_API_KEY` environment variable in `.env` file in the current directory. Or you can give the env file path by `-e` option.

```bash
cat .env
GEMINI_API_KEY=<YOUR_GEMINI_KEY>
```

### Try out the Embedding Models

```bash
# show general usage of emb command.
emb --help

# list all available models.
emb models
GeminiEmbeddingModel
    Vendor: gemini
    Models:
    * gemini-embedding-exp-03-07 (aliases: exp-03-07)
    * text-embedding-004 (aliases: text-004)
    * embedding-001 (aliases: )
    Model Options:
    * task_type (str) - The type of task for the embedding. Supported task types: 'semantic_similarity', 'classification', 'clustering', 'retrieval_document', 'retrieval_query', 'question_answering', 'fact_verification', 'code_retrieval_query'

# get an embedding for an input text by text-embedding-004 model.
emb embed -m text-004 "Embeddings are essential for semantic search and RAG apps."

# get an embedding for an input text by text-embedding-004 model with task_type=retrieval_query.
emb embed -m text-004 "Embeddings are essential for semantic search and RAG apps." -o task_type retrieval_query

# calculate similarity score between two texts by text-embedding-004 model. the default metric is cosine similarity.
emb simscore -m text-004 "The cat drifts toward sleep." "Sleep dances in the cat's eyes."
0.8025767622661093
```

### Document Indexing and Search

You can use the `emb` command to index documents and perform semantic search. `emb` uses [`chroma`](https://github.com/chroma-core/chroma) for the default vector database.

```bash
# index example documents in the current directory.
emb ingest-sample -m text-004 -c catcafe --corpus cat-names

# or, you can give the path to your documents.
# the documents should be in a CSV file with two columns: id and text. the separator should be comma.
emb ingest -m text-004 -c catcafe -f <path-to-your-documents>

# search for a query in the indexed documents.
emb search -m text-004 -c catcafe -q "Who's the naughtiest one?"
Found 5 results:
Score: 0.5264116432711389, Document ID: 28, Text: Loki: Loki is a mischievous and clever cat, always finding new ways to entertain himself, sometimes at his humans' expense. He is a master of stealth and surprise attacks on toys. Despite his playful trickery, Loki is incredibly charming and affectionate, easily winning hearts with his roguish appeal.
Score: 0.5167245254962557, Document ID: 46, Text: Bandit: Bandit is a mischievous cat, often with mask-like markings, always on the lookout for his next playful heist of a toy or treat. He is clever and energetic, loving to chase and pounce. Despite his roguish name, Bandit is a loving companion who enjoys a good cuddle after his adventures.
Score: 0.5093414700625404, Document ID: 76, Text: Frankie: Frankie is a boisterous and playful cat, full of charm and mischief. He loves to zoom around the house and engage in energetic play sessions, especially with crinkly toys. Frankie is also very affectionate, often seeking out his humans for cuddles and purrs after his bursts of energy, a fun-loving friend.
Score: 0.5047165435030156, Document ID: 97, Text: Alfie: Alfie is a cheerful and mischievous little cat, always getting into playful trouble with a charming innocence. He loves exploring small spaces and batting at dangling objects. Alfie is incredibly affectionate, quick to purr and eager for cuddles, a delightful bundle of joy and entertainment for his humans.
Score: 0.5034822716772406, Document ID: 71, Text: Archie: Archie is a friendly and slightly goofy ginger cat, always up for a bit of fun and a good meal. He is very sociable and loves attention from anyone willing to give it. Archie enjoys playful wrestling and will often follow his humans around, offering cheerful chirps and affectionate head-bumps.
```


## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

You need to have a Gemini API key to run the tests for the `embcli-gemini` package. You can set it up as an environment variable:

```bash
GEMINI_API_KEY=<YOUR_GEMINI_KEY> RUN_GEMINI_TESTS=1 uv run --package embcli-gemini pytest packages/embcli-gemini/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-gemini
uv run ruff format packages/embcli-gemini
```

### Run Type Checker

```bash
uv run --package embcli-gemini pyright packages/embcli-gemini
```

## Build

```bash
uv build --package embcli-gemini
```

## License

Apache License 2.0
