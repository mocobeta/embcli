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

**Example usage:** get an embedding for an input image by an original CLIP model.

```bash
# Assume you have an image file `gingercat.jpeg` in the current directory.
emb embed -m clip --image gingercat.jpeg
```