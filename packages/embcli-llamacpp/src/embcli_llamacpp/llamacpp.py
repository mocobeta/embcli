from contextlib import contextmanager, redirect_stderr, redirect_stdout
from os import devnull
from typing import Iterator

import embcli_core
from embcli_core.models import LocalEmbeddingModel
from llama_cpp import Llama


@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, "w") as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


class LlamaCppModel(LocalEmbeddingModel):
    vendor = "llama-cpp"
    default_batch_size = 100
    model_aliases = [("llama-cpp", ["llamacpp"])]
    valid_options = []

    def __init__(self, model_id: str, **kwargs):
        super().__init__(model_id, **kwargs)
        if self.local_model_path is None:
            raise ValueError("model path must be provided for LlamaCppModel.")
        # suppress the output of llama.cpp
        with suppress_stdout_stderr():
            self.model = Llama(model_path=self.local_model_path, embedding=True, vebose=False)

    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float]]:
        if not input:
            return
        # Call LlamaCpp to get embeddings
        # suppress the output of llama.cpp
        with suppress_stdout_stderr():
            embeddings = self.model.create_embedding(input, **kwargs)
        for item in embeddings["data"]:
            yield item["embedding"]  # type: ignore


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str, **kwargs):
        model_ids = [alias[0] for alias in LlamaCppModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return LlamaCppModel(model_id, **kwargs)

    return LlamaCppModel, create
