from typing import Iterator

import embcli_core
import torch
from embcli_core.models import LocalMultimodalEmbeddingModel, Modality
from PIL import Image
from transformers import AutoProcessor, AutoTokenizer  # type: ignore
from transformers import CLIPModel as HFClipModel  # type: ignore


class CLIPModel(LocalMultimodalEmbeddingModel):
    vendor = "clip"
    default_batch_size = 100
    model_aliases = [("clip", [])]
    default_local_model = "openai/clip-vit-base-patch32"
    valid_options = []
    local_model_list = "https://huggingface.co/openai?search_models=clip"

    def __init__(self, model_id: str, **kwargs):
        super().__init__(model_id, **kwargs)
        if self.local_model_id is None:
            self.local_model_id = self.default_local_model
        self.device = "gpu" if torch.cuda.is_available() else "cpu"
        self.model = HFClipModel.from_pretrained(self.local_model_id)

    def _embed_one_batch_multimodal(self, input: list[str], modality: Modality, **kwargs) -> Iterator[list[float]]:
        if not input:
            return

        match modality:
            case Modality.TEXT:
                # Process text input
                tokenizer = AutoTokenizer.from_pretrained(self.local_model_id)
                inputs = tokenizer(input, return_tensors="pt", padding=True, truncation=True).to(self.model.device)
                outputs = self.model.get_text_features(**inputs)
            case Modality.IMAGE:
                # Process image input
                images = [Image.open(img_path) for img_path in input]
                processor = AutoProcessor.from_pretrained(self.local_model_id, use_fast=True)
                inputs = processor(images=images, return_tensors="pt").to(self.model.device)
                outputs = self.model.get_image_features(**inputs)
            case _:
                raise ValueError(f"Unsupported modality: {modality}")

        for tensor in outputs:
            yield tensor.to(self.device).detach().numpy().tolist()


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str, **kwargs):
        model_ids = [alias[0] for alias in CLIPModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return CLIPModel(model_id, **kwargs)

    return CLIPModel, create
