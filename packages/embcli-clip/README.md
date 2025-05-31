# embcli-clip

[![PyPI](https://img.shields.io/pypi/v/embcli-clip?label=PyPI)](https://pypi.org/project/embcli-clip/)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mocobeta/embcli/ci-clip.yml?logo=github&label=tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/embcli-clip)

CLIP plugin for embcli, a command-line interface for embeddings.

## Reference

- [openai/CLIP](https://github.com/openai/CLIP)
- [Hugging Face implementation of CLIP](https://huggingface.co/docs/transformers/model_doc/clip)

## Installation

```bash
pip install embcli-clip
```

## Quick Start


### Try out the Multimodal Embedding Models

desc.txt
```
A ginger cat with bright green eyes, lazily stretching out on a sun-drenched windowsill.
```

gingercat.jpeg
![gingercat.jpeg](gingercat.jpeg)

```bash
# show general usage of emb command.
emb --help

# list all available models.
emb models
CLIPModel
    Vendor: clip
    Models:
    * clip (aliases: )
    See https://huggingface.co/openai?search_models=clip for available local models.
    Model Options:

# get an embedding for an input text by an original CLIP model (openai/clip-vit-base-patch32)
# it'll take a while to download the model from Hugging Face Hub for the first time.
emb embed -m clip -f desc.txt

# get an embedding for an input image by an original CLIP model.
emb embed -m clip --image gingercat.jpeg

# get an embedding model by a community model.
emb embed -m clip/laion/CLIP-ViT-H-14-laion2B-s32B-b79K --image gingercat.jpeg

# calculate similarity score between a text and an image. the default metric is cosine similarity.
emb simscore -m clip -f1 desc.txt --image2 gingercat.jpeg
0.33982698978267567
```

### Document Indexing and Multimodal Search

You can use the `emb` command to index documents and perform search by an image. `emb` uses [`chroma`](https://github.com/chroma-core/chroma) for the default vector database.

```bash
# index example documents in the current directory.
emb ingest-sample -m clip -c catcafe --corpus cat-names-en

# or, you can give the path to your documents.
# the documents should be in a CSV file with two columns: id and text. the separator should be comma.
emb ingest -m clip -c <collection-name> -f <path-to-your-documents>

# search for an image in the indexed documents.
emb search -m clip -c catcafe --image gingercat.jpeg
Found 5 results:
Score: 0.008130492317462625, Document ID: 14, Text: Milo: Milo is an endlessly curious and adventurous orange tabby, always the first to investigate new sounds or objects. He is incredibly friendly, greeting everyone with enthusiastic meows and leg-rubs. Milo loves interactive toys and will happily follow his humans around, eager to be involved in every household activity.
Score: 0.00806729872159855, Document ID: 54, Text: Jasper (II): Jasper the Second, distinct from his predecessor, is a playful and highly energetic ginger tom. He loves to chase, tumble, and explore every nook and cranny with boundless enthusiasm. Jasper is also incredibly affectionate, always ready for a cuddle after a vigorous play session, a bundle of orange joy.
Score: 0.007995471315075445, Document ID: 8, Text: Oliver (Ollie): Ollie is a charmingly goofy orange tabby, full of curious energy and playful pounces. He’s incredibly friendly, often greeting visitors with a cheerful chirp and a head-butt. He loves food, interactive toys, and will happily follow his humans around, always eager to be part of the action.
Score: 0.007992460725066777, Document ID: 71, Text: Archie: Archie is a friendly and slightly goofy ginger cat, always up for a bit of fun and a good meal. He is very sociable and loves attention from anyone willing to give it. Archie enjoys playful wrestling and will often follow his humans around, offering cheerful chirps and affectionate head-bumps.
Score: 0.007982146864511108, Document ID: 42, Text: Sammy: Sammy is a laid-back and friendly ginger cat, always happy to see you. He enjoys lounging in comfortable spots but is also up for a gentle play session. Sammy is a great companion for a relaxed household, offering quiet affection and a warm, purring presence without demanding constant attention.

# or, you can search for a text.
emb search -m clip -c catcafe -q "A lazy ginger cat stretching in the sun"
Found 5 results:
Score: 0.02344505173322954, Document ID: 42, Text: Sammy: Sammy is a laid-back and friendly ginger cat, always happy to see you. He enjoys lounging in comfortable spots but is also up for a gentle play session. Sammy is a great companion for a relaxed household, offering quiet affection and a warm, purring presence without demanding constant attention.
Score: 0.023361588000522227, Document ID: 15, Text: Finn: Finn is a spirited and agile ginger cat, always ready for an adventure. He excels at climbing and exploring high places, often surprising his humans with his acrobatic feats. Playful and energetic, Finn loves interactive games and will keep you entertained with his boundless enthusiasm and charming persistence for play.
Score: 0.0229521169270549, Document ID: 8, Text: Oliver (Ollie): Ollie is a charmingly goofy orange tabby, full of curious energy and playful pounces. He’s incredibly friendly, often greeting visitors with a cheerful chirp and a head-butt. He loves food, interactive toys, and will happily follow his humans around, always eager to be part of the action.
Score: 0.022435629708038293, Document ID: 14, Text: Milo: Milo is an endlessly curious and adventurous orange tabby, always the first to investigate new sounds or objects. He is incredibly friendly, greeting everyone with enthusiastic meows and leg-rubs. Milo loves interactive toys and will happily follow his humans around, eager to be involved in every household activity.
Score: 0.022339791099637154, Document ID: 54, Text: Jasper (II): Jasper the Second, distinct from his predecessor, is a playful and highly energetic ginger tom. He loves to chase, tumble, and explore every nook and cranny with boundless enthusiasm. Jasper is also incredibly affectionate, always ready for a cuddle after a vigorous play session, a bundle of orange joy.
```

## Development

See the [main README](https://github.com/mocobeta/embcli/blob/main/README.md) for general development instructions.

### Run Tests

```bash
RUN_CLIP_TESTS=1 uv run --package embcli-clip pytest packages/embcli-clip/tests/
```

### Run Linter and Formatter

```bash
uv run ruff check --fix packages/embcli-clip
uv run ruff format packages/embcli-clip
```

### Run Type Checker

```bash
uv run --package embcli-clip pyright packages/embcli-clip
```

## Build

```bash
uv build --package embcli-clip
```

## License

Apache License 2.0
