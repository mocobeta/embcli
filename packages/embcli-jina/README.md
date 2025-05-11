# embcli-jina

jina plugin for embcli, a command-line interface for embeddings.

## Reference

- [Jina Models](https://jina.ai/models)

## Installation

```bash
pip install embcli-jina
```

## Quick Start

You need Jina API key to use this plugin. Set `JINA_API_KEY` environment variable in `.env` file in the current directory. Or you can give the env file path by `-e` option.

```bash
cat .env
JINA_API_KEY=<YOUR_JINA_KEY>
```

### Try out the Embedding Models

```bash
# show general usage of emb command.
emb --help

# list all available models.
emb models
JinaEmbeddingModel
    Vendor: jina
    Models:
    * jina-embeddings-v3 (aliases: jina-v3)
    * jina-colbert-v2 (aliases: colbert-v2)
    * jina-embeddings-v2-base-code (aliases: jina-v2-code)
    Model Options:
    * task (str) - Downstream task for which the embeddings are used. Supported tasks: 'text-matching', 'retrieval.query', 'retrieval.passage', 'separation', 'classification'. Only supported in jina-embeddings-v3.
    * late_chunking (bool) - Whether if the late chunking is applied. Only supported in jina-embeddings-v3.
    * truncate (bool) - When enabled, the model will automatically drop the tail that extends beyond the maximum context length allowed by the model instead of throwing an error. Only supported in jina-embeddings-v3.
    * dimensions (int) - The number of dimensions the resulting output embeddings should have. Only supported in jina-embeddings-v3 and jina-colbert-v2.
    * input_type (str) - The type of input to the model. Supported types: 'query', 'document' Only supported in jina-corebert-v2.

# get an embedding for an input text by jina-embeddings-v3 model.
emb embed -m jina-v3 "Embeddings are essential for semantic search and RAG apps."

# get an embedding for an input text by jina-embeddings-v3 model model with dimensions=512.
emb embed -m jina-v3 "Embeddings are essential for semantic search and RAG apps." -o dimensions 512

# calculate similarity score between two texts by jina-embeddings-v3 model model. the default metric is cosine similarity.
emb simscore -m jina-v3 "The cat drifts toward sleep." "Sleep dances in the cat's eyes."
0.708945856730407
```

### Document Indexing and Search

You can use the `emb` command to index documents and perform semantic search. `emb` uses [`chroma`](https://github.com/chroma-core/chroma) for the default vector database.

```bash
# index example documents in the current directory.
emb ingest-sample -m jina-v3 -c catcafe --corpus cat-names

# or, you can give the path to your documents.
# the documents should be in a CSV file with two columns: id and text. the separator should be comma.
emb ingest -m jina-v3 -c catcafe -f <path-to-your-documents>

# search for a query in the indexed documents.
emb search -m jina-v3 -c catcafe -q "Who's the naughtiest one?"
Found 5 results:
Score: 0.45097012297560646, Document ID: 12, Text: Leo: Leo, with his magnificent mane-like ruff, carries himself with regal confidence. He is a natural leader, often surveying his domain from the highest point in the room. Affectionate on his own terms, Leo enjoys a good chin scratch and will reward loyalty with his rumbling purr and majestic presence.
Score: 0.4291541094385421, Document ID: 46, Text: Bandit: Bandit is a mischievous cat, often with mask-like markings, always on the lookout for his next playful heist of a toy or treat. He is clever and energetic, loving to chase and pounce. Despite his roguish name, Bandit is a loving companion who enjoys a good cuddle after his adventures.
Score: 0.4137949268906759, Document ID: 20, Text: Pepper: Pepper is a feisty and energetic grey tabby with a spicy personality. She is quick-witted and loves to engage in playful stalking and pouncing games. Pepper is also fiercely independent but will show her affection with sudden bursts of purring and head-butts, keeping her humans on their toes.
Score: 0.40369800611316564, Document ID: 35, Text: Lucy: Lucy is a sweet-natured and playful cat, often a ginger or calico, with a bright personality. She loves attention and will often seek out her humans for cuddles and playtime. Lucy is very expressive, using chirps and meows to communicate her desires, her joyful spirit lighting up the household.
Score: 0.4031877012247693, Document ID: 3, Text: Pippin (Pip): Pippin, or Pip, is a compact dynamo, brimming with mischievous charm and boundless curiosity. He’s an intrepid explorer, always finding new hideouts or investigating forbidden territories with a twinkle in his eye. Quite vocal, Pip will happily chat about his day, his playful antics making him an endearing little rascal.
```

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

You need to have a Jina API key to run the tests for the `embcli-jina` package. You can set it up as an environment variable:

```bash
JINA_API_KEY=<YOUR_JINA_KEY> RUN_JINA_TESTS=1 uv run --package embcli-jina pytest packages/embcli-jina/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-jina
uv run ruff format packages/embcli-jina
```

### Run Type Checker

```bash
uv run --package embcli-jina pyright packages/embcli-jina
```

## Build

```bash
uv build --package embcli-jina
```

## License

Apache License 2.0
