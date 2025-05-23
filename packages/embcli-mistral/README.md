# embcli-mistral

[![PyPI](https://img.shields.io/pypi/v/embcli-mistral?label=PyPI)](https://pypi.org/project/embcli-mistral/)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mocobeta/embcli/ci-mistral.yml?logo=github&label=tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/embcli-mistral)

mistral plugin for embcli, a command-line interface for embeddings.

## Reference

- [Mistral Embeddings](https://docs.mistral.ai/capabilities/embeddings/)

## Installation

```bash
pip install embcli-mistral
```

## Quick Start

You need Mistral API key to use this plugin. Set `MISTRAL_API_KEY` environment variable in `.env` file in the current directory. Or you can give the env file path by `-e` option.

```bash
cat .env
MISTRAL_API_KEY=<YOUR_MISTRAL_KEY>
```

### Try out the Embedding Models

```bash
# show general usage of emb command.
emb --help

# list all available models.
emb models
MistralEmbeddingModel
    Vendor: mistral
    Models:
    * mistral-embed (aliases: )
    Model Options:

# get an embedding for an input text by mistral-embed model.
emb embed -m mistral-embed "Embeddings are essential for semantic search and RAG apps."

# calculate similarity score between two texts by mistral-embed model. the default metric is cosine similarity.
emb simscore -m mistral-embed "The cat drifts toward sleep." "Sleep dances in the cat's eyes."
0.8912508450525568
```

### Document Indexing and Search

You can use the `emb` command to index documents and perform semantic search. `emb` uses [`chroma`](https://github.com/chroma-core/chroma) for the default vector database.

```bash
# index example documents in the current directory.
emb ingest-sample -m mistral-embed -c catcafe --corpus cat-names-en

# or, you can give the path to your documents.
# the documents should be in a CSV file with two columns: id and text. the separator should be comma.
emb ingest -m mistral-embed -c catcafe -f <path-to-your-documents>

# search for a query in the indexed documents.
emb search -m mistral-embed -c catcafe -q "Who's the naughtiest one?"
Found 5 results:
Score: 0.6517009284006381, Document ID: 76, Text: Frankie: Frankie is a boisterous and playful cat, full of charm and mischief. He loves to zoom around the house and engage in energetic play sessions, especially with crinkly toys. Frankie is also very affectionate, often seeking out his humans for cuddles and purrs after his bursts of energy, a fun-loving friend.
Score: 0.6514949046818957, Document ID: 46, Text: Bandit: Bandit is a mischievous cat, often with mask-like markings, always on the lookout for his next playful heist of a toy or treat. He is clever and energetic, loving to chase and pounce. Despite his roguish name, Bandit is a loving companion who enjoys a good cuddle after his adventures.
Score: 0.6456183753007453, Document ID: 20, Text: Pepper: Pepper is a feisty and energetic grey tabby with a spicy personality. She is quick-witted and loves to engage in playful stalking and pouncing games. Pepper is also fiercely independent but will show her affection with sudden bursts of purring and head-butts, keeping her humans on their toes.
Score: 0.645051423128062, Document ID: 97, Text: Alfie: Alfie is a cheerful and mischievous little cat, always getting into playful trouble with a charming innocence. He loves exploring small spaces and batting at dangling objects. Alfie is incredibly affectionate, quick to purr and eager for cuddles, a delightful bundle of joy and entertainment for his humans.
Score: 0.6441489894320535, Document ID: 40, Text: Jack: Jack is a charming and roguish cat, often a black and white tuxedo, full of personality. He is clever and resourceful, always finding new ways to entertain himself. Jack enjoys playful interactions and can be quite vocal, always ready with a friendly meow or a playful swat at a toy.

# multilingual search
emb search -m mistral-embed -c catcafe -q "一番のいたずら者は誰?"
Found 5 results:
Score: 0.6155281401556078, Document ID: 95, Text: Yoshi: Yoshi is a playful and endearing cat, often with a slightly goofy charm that wins everyone over. He loves interactive toys, especially those he can chase and pounce on. Yoshi is very affectionate, always eager for a pet or a warm lap, his happy purrs filling the room.
Score: 0.6122135784501259, Document ID: 28, Text: Loki: Loki is a mischievous and clever cat, always finding new ways to entertain himself, sometimes at his humans' expense. He is a master of stealth and surprise attacks on toys. Despite his playful trickery, Loki is incredibly charming and affectionate, easily winning hearts with his roguish appeal.
Score: 0.6099866660529429, Document ID: 46, Text: Bandit: Bandit is a mischievous cat, often with mask-like markings, always on the lookout for his next playful heist of a toy or treat. He is clever and energetic, loving to chase and pounce. Despite his roguish name, Bandit is a loving companion who enjoys a good cuddle after his adventures.
Score: 0.6097906319162568, Document ID: 70, Text: Zeke: Zeke is a zesty and energetic cat, always on the move and looking for fun. He loves to play, chase, and explore, bringing a lot of life to his home. Zeke is also very friendly and enjoys interacting with his humans, often greeting them with enthusiastic meows and playful antics.
Score: 0.6082587693891089, Document ID: 10, Text: Mochi: Mochi is a delightfully round and fluffy cat, as sweet and soft as her namesake. She is a champion napper, always seeking the warmest, coziest spot for a snooze. A true lap cat, Mochi's gentle purr is a constant, comforting presence, and she adores soft pets and chin scratches.
```

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

You need to have a Mistral API key to run the tests for the `embcli-mistral` package. You can set it up as an environment variable:

```bash
MISTRAL_API_KEY=<YOUR_MISTRAL_KEY> RUN_MISTRAL_TESTS=1 uv run --package embcli-mistral pytest packages/embcli-mistral/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-mistral
uv run ruff format packages/embcli-mistral
```

### Run Type Checker

```bash
uv run --package embcli-mistral pyright packages/embcli-mistral
```

## Build

```bash
uv build --package embcli-mistral
```

## License

Apache License 2.0
