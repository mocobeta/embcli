# embcli-openai

openai plugin for embcli, a command-line interface for embeddings.

## Reference

- [OpenAI Models](https://platform.openai.com/docs/models)

## Installation

```bash
pip install embcli-openai
```

## Quick Start

You need OpenAI API key to use this plugin. Set `OPENAI_API_KEY` environment variable in `.env` file in the current directory. Or you can give the env file path by `-e` option.

```bash
cat .env
OPENAI_API_KEY=<YOUR_OPENAI_KEY>
```

### Try out the Embedding Models

```bash
# show general usage of emb command.
emb --help

# list all available models.
emb models
OpenAIEmbeddingModel
    Vendor: openai
    Models:
    * text-embedding-3-small (aliases: 3-small)
    * text-embedding-3-large (aliases: 3-large)
    * text-embedding-ada-002 (aliases: ada-002)
    Model Options:
    * dimensions (int) - The number of dimensions the resulting output embeddings should have. Only supported in text-embedding-3 and later models.

# get an embedding for an input text by text-embedding-3-small model.
emb embed -m 3-small "Embeddings are essential for semantic search and RAG apps."

# get an embedding for an input text by text-embedding-3-small model with dimensions=512.
emb embed -m 3-small "Embeddings are essential for semantic search and RAG apps." -o dimensions 512

# calculate similarity score between two texts by text-embedding-3-small model. the default metric is cosine similarity.
emb simscore -m 3-small "The cat drifts toward sleep." "Sleep dances in the cat's eyes."
0.6082515648413913
```

### Document Indexing and Search

You can use the `emb` command to index documents and perform semantic search. `emb` uses [`chroma`](https://github.com/chroma-core/chroma) for the default vector database.

```bash
# index example documents in the current directory.
emb ingest-sample -m 3-small -c catcafe --corpus cat-names

# or, you can give the path to your documents.
# the documents should be in a CSV file with two columns: id and text. the separator should be comma.
emb ingest -m 3-small -c catcafe -f <path-to-your-documents>

# search for a query in the indexed documents.
emb search -m 3-small -c catcafe -q "Who's the naughtiest one?"
Found 5 results:
Score: 0.4130458064043753, Document ID: 20, Text: Pepper: Pepper is a feisty and energetic grey tabby with a spicy personality. She is quick-witted and loves to engage in playful stalking and pouncing games. Pepper is also fiercely independent but will show her affection with sudden bursts of purring and head-butts, keeping her humans on their toes.
Score: 0.41092058398810277, Document ID: 72, Text: Bea: Bea is a sweet and gentle calico, as lovely as a busy bee in a garden. She enjoys quiet observation and sunbathing, but also has a playful side, especially with feather wands. Bea is affectionate and loves a warm lap, her soft purrs a comforting hum, a truly delightful companion.
Score: 0.4099998098731923, Document ID: 25, Text: Nala: Nala is a graceful and queenly cat, often a beautiful cream or light tan color. She moves with quiet dignity and observes her surroundings with intelligent eyes. Nala is affectionate but discerning, choosing her moments for cuddles, and her loyalty to her family is unwavering, a truly regal companion.
Score: 0.40864073184452354, Document ID: 97, Text: Alfie: Alfie is a cheerful and mischievous little cat, always getting into playful trouble with a charming innocence. He loves exploring small spaces and batting at dangling objects. Alfie is incredibly affectionate, quick to purr and eager for cuddles, a delightful bundle of joy and entertainment for his humans.
Score: 0.4081247525728411, Document ID: 46, Text: Bandit: Bandit is a mischievous cat, often with mask-like markings, always on the lookout for his next playful heist of a toy or treat. He is clever and energetic, loving to chase and pounce. Despite his roguish name, Bandit is a loving companion who enjoys a good cuddle after his adventures.
```

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
