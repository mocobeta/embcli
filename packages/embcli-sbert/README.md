# embcli-sbert

[![PyPI](https://img.shields.io/pypi/v/embcli-sbert?label=PyPI)](https://pypi.org/project/embcli-sbert/)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mocobeta/embcli/ci-sbert.yml?logo=github&label=tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/embcli-sbert)

sbert (sentence-transformers) plugin for embcli, a command-line interface for embeddings.

## Reference

- [SentenceTransformers](https://sbert.net/index.html)

## Installation

```bash
pip install embcli-sbert
```

## Quick Start


### Try out the Embedding Models

```bash
# show general usage of emb command.
emb --help

# list all available models.
emb models
SentenceTransformerModel
    Vendor: sbert
    Models:
    * sentence-transformers (aliases: sbert)
    See https://sbert.net/docs/sentence_transformer/pretrained_models.html for available models.
    Model Options:

# get an embedding for an input text by an original sentence-transformers model (e.g. all-MiniLM-L6-v2).
# it'll take a while to download the model from Hugging Face Hub for the first time.
emb embed -m sbert/all-MiniLM-L6-v2 "Embeddings are essential for semantic search and RAG apps."

# get an embedding model by a community model.
emb embed -m sbert/intfloat/multilingual-e5-small "Embeddings are essential for semantic search and RAG apps."

# calculate similarity score between two texts by all-MiniLM-L6-v2. the default metric is cosine similarity.
emb simscore -m sbert/all-MiniLM-L6-v2 "The cat drifts toward sleep." "Sleep dances in the cat's eyes."
0.8031787421988659
```

### Document Indexing and Search

You can use the `emb` command to index documents and perform semantic search. `emb` uses [`chroma`](https://github.com/chroma-core/chroma) for the default vector database.

```bash
# index example documents in the current directory.
emb ingest-sample -m sbert/all-MiniLM-L6-v2 -c catcafe --corpus cat-names-en

# or, you can give the path to your documents.
# the documents should be in a CSV file with two columns: id and text. the separator should be comma.
emb ingest -m sbert/all-MiniLM-L6-v2 -c catcafe -f <path-to-your-documents>

# search for a query in the indexed documents.
emb search -m sbert/all-MiniLM-L6-v2 -c catcafe -q "Who's the naughtiest one?"
Found 5 results:
Score: 0.3956756932171536, Document ID: 25, Text: Nala: Nala is a graceful and queenly cat, often a beautiful cream or light tan color. She moves with quiet dignity and observes her surroundings with intelligent eyes. Nala is affectionate but discerning, choosing her moments for cuddles, and her loyalty to her family is unwavering, a truly regal companion.
Score: 0.39523976965995117, Document ID: 12, Text: Leo: Leo, with his magnificent mane-like ruff, carries himself with regal confidence. He is a natural leader, often surveying his domain from the highest point in the room. Affectionate on his own terms, Leo enjoys a good chin scratch and will reward loyalty with his rumbling purr and majestic presence.
Score: 0.3918249967723957, Document ID: 32, Text: Max: Max is a quintessential friendly cat, often a sturdy tabby, who is easygoing and loves everyone. He is playful in a relaxed way, enjoying a good game of chase-the-string but equally happy to lounge nearby. Max is a dependable companion, always ready with a comforting purr and a friendly nuzzle.
Score: 0.3913900431393664, Document ID: 54, Text: Jasper (II): Jasper the Second, distinct from his predecessor, is a playful and highly energetic ginger tom. He loves to chase, tumble, and explore every nook and cranny with boundless enthusiasm. Jasper is also incredibly affectionate, always ready for a cuddle after a vigorous play session, a bundle of orange joy.
Score: 0.38631855385121966, Document ID: 36, Text: Oscar: Oscar is a distinguished and somewhat opinionated cat, often a grumpy-looking but secretly soft Persian. He has his routines and prefers things a certain way but is deeply affectionate with his family. Oscar enjoys luxurious naps and will reward his humans with rumbling purrs when properly pampered.

# multilingual search
emb search -m sbert/all-MiniLM-L6-v2 -c catcafe -q "一番のいたずら者は誰?"
Found 5 results:
Score: 0.3771080195010235, Document ID: 68, Text: Xavi: Xavi is an intelligent and agile cat, perhaps a sleek black or Oriental breed, quick on his feet and sharp in mind. He enjoys interactive toys that challenge him and loves to explore high places. Xavi is affectionate with his family, often engaging them in playful banter or quiet cuddles.
Score: 0.376757642611273, Document ID: 95, Text: Yoshi: Yoshi is a playful and endearing cat, often with a slightly goofy charm that wins everyone over. He loves interactive toys, especially those he can chase and pounce on. Yoshi is very affectionate, always eager for a pet or a warm lap, his happy purrs filling the room.
Score: 0.37384416079962984, Document ID: 81, Text: Kai: Kai is a sleek and agile cat, perhaps with exotic origins, possessing a cool and composed demeanor. He is an excellent hunter of toys and enjoys surveying his domain from high perches. Kai is affectionate with his trusted humans, offering quiet companionship and a rumbling purr, a mysteriously charming feline.
Score: 0.373308241432645, Document ID: 48, Text: Winston: Winston is a distinguished and thoughtful cat, perhaps a British Shorthair, with a calm and composed demeanor. He enjoys observing his surroundings from a comfortable perch and appreciates a predictable routine. Winston is a loyal and affectionate companion, offering quiet comfort and steadfast friendship to his household.
Score: 0.37157731687555895, Document ID: 88, Text: Remi: Remi is a charming and artistic soul, perhaps a cat with unique markings or a flair for dramatic poses. He is playful and enjoys creative games, often inventing his own. Remi is also very affectionate, loving to cuddle and purr, bringing a touch of whimsy and love to his home.
```

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

```bash
RUN_SBERT_TESTS=1 uv run --package embcli-sbert pytest packages/embcli-sbert/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-sbert
uv run ruff format packages/embcli-sbert
```

### Run Type Checker

```bash
uv run --package embcli-sbert pyright packages/embcli-sbert
```

## Build

```bash
uv build --package embcli-sbert
```

## License

Apache License 2.0
