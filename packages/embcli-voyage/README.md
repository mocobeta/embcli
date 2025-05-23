# embcli-voyage

[![PyPI](https://img.shields.io/pypi/v/embcli-voyage?label=PyPI)](https://pypi.org/project/embcli-voyage/)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mocobeta/embcli/ci-voyage.yml?logo=github&label=tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/embcli-voyage)

voyage plugin for embcli, a command-line interface for embeddings.

## Reference

- [VoyageAI Text Embeddings](https://docs.voyageai.com/docs/embeddings)

## Installation

```bash
pip install embcli-voyage
```

## Quick Start

You need VoyageAI API key to use this plugin. Set `VOYAGE_API_KEY` environment variable in `.env` file in the current directory. Or you can give the env file path by `-e` option.

```bash
cat .env
VOYAGE_API_KEY=<YOUR_VOYAGE_KEY>
```

### Try out the Embedding Models

```bash
# show general usage of emb command.
emb --help

# list all available models.
emb models
VoyageEmbeddingModel
    Vendor: voyage
    Models:
    * voyage-3-large (aliases: )
    * voyage-3 (aliases: )
    * voyage-3-lite (aliases: )
    * voyage-code-3 (aliases: )
    * voyage-finance-2 (aliases: )
    * voyage-law-2 (aliases: )
    * voyage-code-2 (aliases: )
    Model Options:
    * input_type (str) - Type of the input text. Options: 'None', 'query', 'document' Defaults to 'None'.
    * truncation (bool) - Whether to truncate the input texts to fit within the context length. Defaults to True.
    * output_dimension (int) - The number of dimensions for resulting output embeddings.

# get an embedding for an input text by voyage-3 model.
emb embed -m voyage-3 "Embeddings are essential for semantic search and RAG apps."

# get an embedding for an input text by voyage-3 model with input_type=query.
emb embed -m voyage-3 "Embeddings are essential for semantic search and RAG apps." -o input_type query

# calculate similarity score between two texts by voyage-3 model. the default metric is cosine similarity.
emb simscore -m voyage-3 "The cat drifts toward sleep." "Sleep dances in the cat's eyes."
0.7499687978192594
```

### Document Indexing and Search

You can use the `emb` command to index documents and perform semantic search. `emb` uses [`chroma`](https://github.com/chroma-core/chroma) for the default vector database.

```bash
# index example documents in the current directory.
emb ingest-sample -m voyage-3 -c catcafe --corpus cat-names-en

# or, you can give the path to your documents.
# the documents should be in a CSV file with two columns: id and text. the separator should be comma.
emb ingest -m voyage-3 -c catcafe -f <path-to-your-documents>

# search for a query in the indexed documents.
emb search -m voyage-3 -c catcafe -q "Who's the naughtiest one?"
Found 5 results:
Score: 0.41797321996324216, Document ID: 28, Text: Loki: Loki is a mischievous and clever cat, always finding new ways to entertain himself, sometimes at his humans' expense. He is a master of stealth and surprise attacks on toys. Despite his playful trickery, Loki is incredibly charming and affectionate, easily winning hearts with his roguish appeal.
Score: 0.41704222853043194, Document ID: 46, Text: Bandit: Bandit is a mischievous cat, often with mask-like markings, always on the lookout for his next playful heist of a toy or treat. He is clever and energetic, loving to chase and pounce. Despite his roguish name, Bandit is a loving companion who enjoys a good cuddle after his adventures.
Score: 0.4138587234705962, Document ID: 3, Text: Pippin (Pip): Pippin, or Pip, is a compact dynamo, brimming with mischievous charm and boundless curiosity. He’s an intrepid explorer, always finding new hideouts or investigating forbidden territories with a twinkle in his eye. Quite vocal, Pip will happily chat about his day, his playful antics making him an endearing little rascal.
Score: 0.4102669442076908, Document ID: 66, Text: Vinnie: Vinnie is a cool and confident cat, often a street-smart tabby with a lot of personality. He is resourceful and independent but also enjoys affection from his trusted humans. Vinnie is a survivor with a soft side, offering gruff purrs and head-butts, a charming rogue with a heart of gold.
Score: 0.407675485063674, Document ID: 94, Text: Xena: Xena is a warrior princess of a cat, bold, adventurous, and fiercely protective of her territory and toys. She is highly energetic and loves vigorous play, often surprising with her agility. Despite her tough exterior, Xena is deeply loyal and affectionate to her trusted human companions.

# multilingual search
emb search -m voyage-3 -c catcafe -q "一番のいたずら者は誰?"
Found 5 results:
Score: 0.3996864870685445, Document ID: 5, Text: Cosmo: Cosmo, with his wide, knowing eyes, seems to ponder the universe's mysteries. He’s an endearingly quirky character, often found investigating unusual objects or engaging in peculiar solo games. Highly intelligent and observant, Cosmo loves exploring new spaces, and his quiet, thoughtful nature makes him a fascinating and unique companion.
Score: 0.39843294400750984, Document ID: 83, Text: Monty: Monty is a charming and slightly eccentric cat, full of character and amusing quirks. He might have a favorite unusual napping spot or a peculiar way of playing. Monty is very entertaining and loves attention, often performing his unique antics for his amused human audience, a delightful and unique friend.
Score: 0.39798067438127693, Document ID: 75, Text: Elwood: Elwood is an endearingly quirky and laid-back cat, often found in amusing sleeping positions. He is friendly and easygoing, enjoying simple pleasures like a good meal and a sunny spot. Elwood is a comforting presence, always ready with a soft purr and a gentle nuzzle, a truly chill companion.
Score: 0.39575622315523173, Document ID: 24, Text: Gizmo: Gizmo is an endearingly quirky cat, full of curious habits and playful antics. He might bat at imaginary foes or carry his favorite small toy everywhere. Gizmo is incredibly entertaining and loves attention, often performing his unique tricks for his amused human audience, always bringing a smile.
Score: 0.3932879962838197, Document ID: 50, Text: Dexter: Dexter is a clever and sometimes quirky cat, always up to something interesting. He might have a fascination with running water or a particular toy he carries everywhere. Dexter is highly intelligent and enjoys interactive play, keeping his humans entertained with his unique personality and amusing antics, a truly engaging companion.
```


## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

You need to have a Voyage API key to run the tests for the `embcli-voyage` package. You can set it up as an environment variable:

```bash
VOYAGE_API_KEY=<YOUR_VOYAGE_KEY> RUN_VOYAGE_TESTS=1 uv run --package embcli-voyage pytest packages/embcli-voyage/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-voyage
uv run ruff format packages/embcli-voyage
```

### Run Type Checker

```bash
uv run --package embcli-voyage pyright packages/embcli-voyage
```

## Build

```bash
uv build --package embcli-voyage
```

## License

Apache License 2.0
