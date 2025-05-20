from embcli_core.models import LocalEmbeddingModel


class LlamaCppModel(LocalEmbeddingModel):
    vendor = "llama-cpp"
    default_batch_size = 100
    model_aliases = ["llama-cpp", ["llamacpp"]]
    valid_options = []
