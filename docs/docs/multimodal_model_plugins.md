# Multimodal Model Plugins

A multimodal model plugin is a Python package for a specific multimodal embedding model or model vendor. All model plugins contain the same set of commands, and multiple model plugins can be simultaneously installed in the same environment.

## [embcli-clip](https://pypi.org/project/embcli-clip/) for CLIP Models

The `embcli-clip` plugin provides access to locally installed [CLIP](https://github.com/openai/CLIP) models.

**Installation:** `pip install embcli-clip`

`emb models` command shows the available models with their short aliases and supported model options.

```bash
emb models
CLIPModel
    Vendor: clip
    Models:
    * clip (aliases: )
    See https://huggingface.co/openai?search_models=clip for available local models.
    Model Options:
```

**Example usage:** get an embedding for an input text by a CLIP model.

```bash
# get an embedding for an input text by a CLIP model.
# the default model is `openai/clip-vit-base-patch32`.
emb embed -m clip "Owls can rotate their necks 270 degrees without injury🦉"
```

**Example usage:** get an embedding for an input image by a CLIP model.

```bash
# Assume you have an image file `gingercat.jpeg` in the current directory.
# get an embedding for an input image by the original CLIP model.
emb embed -m clip --image gingercat.jpeg

# get an embedding model by a community model.
emb embed -m clip/laion/CLIP-ViT-H-14-laion2B-s32B-b79K --image gingercat.jpeg
```

## [embcli-jina](https://pypi.org/project/embcli-jina/) for Jina Clip Models

The `embcli-jina` plugin provides access to [Jina's CLIP v2 model](https://jina.ai/news/jina-clip-v2-multilingual-multimodal-embeddings-for-text-and-images/) as well as text embeddings.

You need a Jina API key to use this plugin. Set the `JINA_API_KEY` environment variable in a `.env` file in the current directory, or specify the path to the env file using the `-e` option.

```bash
cat .env
JINA_API_KEY=<YOUR_JINA_KEY>
```

**Installation:** `pip install embcli-jina`

`emb models` command shows the available models with their short aliases and supported model options.

```bash
emb models
JinaEmbeddingModel
    Vendor: jina
... (snip)
JinaClipModel
    Vendor: jina
    Models:
    * jina-clip-v2 (aliases: )
    Model Options:
    * task (str) - Downstream task for which the embeddings are used. Supported tasks: 'retrieval.query', 'retrieval.passage'.
    * dimensions (int) - The number of dimensions the resulting output embeddings should have.
    * embedding_type (str) - The type of embeddings to return. Options include 'float', 'binary', 'ubinary'. Default is 'float'.
```

**Example usage:** get an embedding for an input text by jina-clip-v2 model model with an option dimensions=512 and embedding_type=binary.

```bash
emb embed -m jina-clip-v2 -o dimensions 512 \
-o embedding_type binary \
"Owls can rotate their necks 270 degrees without injury🦉"
```

**Example usage:** get an embedding for an input image by jina-clip-v2 model.

```bash
# Assume you have an image file `gingercat.jpeg` in the current directory.
emb embed -m jina-clip-v2 --image gingercat.jpeg
```

## [embcli-voyage](https://pypi.org/project/embcli-voyage/) for Voyage Multimodal Embeddings

The `embcli-voyage` plugin provides access to [VoyageAI's multimodal embeddings](https://docs.voyageai.com/docs/multimodal-embeddings) as well as text embeddings.

You need a VoyageAI API key to use this plugin. Set the `VOYAGE_API_KEY` environment variable in a `.env` file in the current directory, or specify the path to the env file using the `-e` option.

```bash
cat .env
VOYAGE_API_KEY=<YOUR_VOYAGE_KEY>
```

**Installation:** `pip install embcli-voyage`

`emb models` command shows the available models with their short aliases and supported model options.

```bash
emb models
VoyageEmbeddingModel
    Vendor: voyage
... (snip)
VoyageMultimodalEmbeddingModel
    Vendor: voyage
    Models:
    * voyage-multimodal-3 (aliases: voyage-mm-3)
    Model Options:
    * input_type (str) - Type of the input text. Options: 'None', 'query', 'document' Defaults to 'None'.
    * truncation (bool) - Whether to truncate the input texts to fit within the context length. Defaults to True.
```

**Example usage:** get an embedding for an input text by voyage-multimodal-3 model model with an option `input_type=query`.

```bash
emb embed -m voyage-mm-3 -o input_type query \
"Owls can rotate their necks 270 degrees without injury🦉"
```

**Example usage:** get an embedding for an input image by voyage-multimodal-3 model.

```bash
# Assume you have an image file `gingercat.jpeg` in the current directory.
emb embed -m voyage-mm-3 --image gingercat.jpeg
```
