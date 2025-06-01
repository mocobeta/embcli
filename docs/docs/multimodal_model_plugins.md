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

The `embcli-jina` plugin provides access to [Jina's embedding models](https://jina.ai/models).

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
```

**Example usage:** get an embedding for an input text by jina-clip-v2 model model with an option dimensions=512.

```bash
emb embed -m jina-clip-v2 -o dimensions 512 \
"Owls can rotate their necks 270 degrees without injury🦉"
```

**Example usage:** get an embedding for an input image by jina-clip-v2 model.

```bash
# Assume you have an image file `gingercat.jpeg` in the current directory.
emb embed -m jina-clip-v2 --image gingercat.jpeg
```
