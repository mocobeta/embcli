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