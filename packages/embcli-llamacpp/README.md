# embcli-llamacpp

[![PyPI](https://img.shields.io/pypi/v/embcli-llamacpp?label=PyPI)](https://pypi.org/project/embcli-llamacpp/)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mocobeta/embcli/ci-llamacpp.yml?logo=github&label=tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/embcli-llamacpp)

llama-cpp plugin for embcli, a command-line interface for embeddings. This is a thin wrapper around llama-cpp-python.

## Reference

- [llama-cpp-python](https://llama-cpp-python.readthedocs.io/en/latest/)

## Installation

```bash
pip install embcli-llamacpp
```

## Quick Start

You need to have `gguf` model files in your local machine.

See [this tutorial](https://github.com/ggml-org/llama.cpp/discussions/7712) for instructions on how to convert original Hugging Face transformer models to `gguf` format.

### Try out the Embedding Models

```bash
# show general usage of emb command.
emb --help

# list all available models.
emb models
LlamaCppModel
    Vendor: llama-cpp
    Models:
    * llama-cpp (aliases: llamacpp)
    Model Options:

# assume you have a GGUF converted all-MiniLM-L6-v2 model in the current directory.
# get an embedding for an input text by running the GGUF converted model.
emb embed -m llamacpp -p ./all-MiniLM-L6-v2.F16.gguf "Embeddings are essential for semantic search and RAG apps."

# calculate similarity score between two texts by GGUF converted all-MiniLM-L6-v2 model. the default metric is cosine similarity.
emb simscore -m llamacpp -p ./all-MiniLM-L6-v2.F16.gguf "The cat drifts toward sleep." "Sleep dances in the cat's eyes."
0.8031107247483075
```

### Document Indexing and Search

You can use the `emb` command to index documents and perform semantic search. `emb` uses [`chroma`](https://github.com/chroma-core/chroma) for the default vector database.

```bash
# index example documents in the current directory.
emb ingest-sample -m llamacpp -p ./all-MiniLM-L6-v2.F16.gguf -c catcafe --corpus cat-names-en

# or, you can give the path to your documents.
# the documents should be in a CSV file with two columns: id and text. the separator should be comma.
emb ingest -m llamacpp -p ./all-MiniLM-L6-v2.F16.gguf -c catcafe -f <path-to-your-documents>

# search for a query in the indexed documents.
emb search -m llamacpp -p ./all-MiniLM-L6-v2.F16.gguf -c catcafe -q "Who's the naughtiest one?"
Found 5 results:
Score: 0.03687787040089618, Document ID: 25, Text: Nala: Nala is a graceful and queenly cat, often a beautiful cream or light tan color. She moves with quiet dignity and observes her surroundings with intelligent eyes. Nala is affectionate but discerning, choosing her moments for cuddles, and her loyalty to her family is unwavering, a truly regal companion.
Score: 0.036599260961425885, Document ID: 73, Text: Cody: Cody is a ruggedly handsome tabby, adventurous and brave, always ready to explore new territories. He is curious about everything and enjoys interactive play that mimics hunting. Cody is also a loyal companion, offering strong head-butts and rumbling purrs to show his affection and contentment with his family.
Score: 0.036555873965458334, Document ID: 5, Text: Cosmo: Cosmo, with his wide, knowing eyes, seems to ponder the universe's mysteries. He’s an endearingly quirky character, often found investigating unusual objects or engaging in peculiar solo games. Highly intelligent and observant, Cosmo loves exploring new spaces, and his quiet, thoughtful nature makes him a fascinating and unique companion.
Score: 0.03654979851488558, Document ID: 54, Text: Jasper (II): Jasper the Second, distinct from his predecessor, is a playful and highly energetic ginger tom. He loves to chase, tumble, and explore every nook and cranny with boundless enthusiasm. Jasper is also incredibly affectionate, always ready for a cuddle after a vigorous play session, a bundle of orange joy.
Score: 0.03652978471877379, Document ID: 12, Text: Leo: Leo, with his magnificent mane-like ruff, carries himself with regal confidence. He is a natural leader, often surveying his domain from the highest point in the room. Affectionate on his own terms, Leo enjoys a good chin scratch and will reward loyalty with his rumbling purr and majestic presence.

# multilingual search
emb search -m llamacpp -p ./all-MiniLM-L6-v2.F16.gguf -c catcafe -q "一番のいたずら者は誰?"
Found 5 results:
Score: 0.032483805278333354, Document ID: 81, Text: Kai: Kai is a sleek and agile cat, perhaps with exotic origins, possessing a cool and composed demeanor. He is an excellent hunter of toys and enjoys surveying his domain from high perches. Kai is affectionate with his trusted humans, offering quiet companionship and a rumbling purr, a mysteriously charming feline.
Score: 0.03243122604098391, Document ID: 51, Text: Fiona: Fiona is a charming and slightly regal cat, perhaps with long, flowing fur. She enjoys being pampered but is also playful and adventurous when the mood strikes. Fiona is affectionate with her chosen humans, offering gentle purrs and head-boops, expecting adoration in return for her delightful company and elegant presence.
Score: 0.03229731905787494, Document ID: 95, Text: Yoshi: Yoshi is a playful and endearing cat, often with a slightly goofy charm that wins everyone over. He loves interactive toys, especially those he can chase and pounce on. Yoshi is very affectionate, always eager for a pet or a warm lap, his happy purrs filling the room.
Score: 0.0319359546105567, Document ID: 48, Text: Winston: Winston is a distinguished and thoughtful cat, perhaps a British Shorthair, with a calm and composed demeanor. He enjoys observing his surroundings from a comfortable perch and appreciates a predictable routine. Winston is a loyal and affectionate companion, offering quiet comfort and steadfast friendship to his household.
Score: 0.03189893349379499, Document ID: 34, Text: Charlie: Charlie is an affable and curious cat, often seen exploring every corner of the house with an inquisitive tilt to his head. He is friendly with everyone he meets, humans and other pets alike. Charlie enjoys interactive toys and will happily engage in playful banter, a truly sociable feline.
```

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

```bash
RUN_LLAMACPP_TESTS=1 uv run --package embcli-llamacpp pytest packages/embcli-llamacpp/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-llamacpp
uv run ruff format packages/embcli-llamacpp
```

### Run Type Checker

```bash
uv run --package embcli-llamacpp pyright packages/embcli-llamacpp
```

## Build

```bash
uv build --package embcli-llamacpp
```

## License

Apache License 2.0
