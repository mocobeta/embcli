import pytest
from embcli_core.models import (
    EmbeddingModel,
    LocalEmbeddingModel,
    LocalMultimodalEmbeddingModel,
    Modality,
    MultimodalEmbeddingModel,
    avaliable_models,
    get_model,
    register,
)


def test_initialize_model(mock_model, mock_local_model):
    assert mock_model.model_id == "embedding-mock-1"

    assert mock_local_model.model_id == "local-embedding-mock"
    assert mock_local_model.local_model_id == "mymodel"
    assert mock_local_model.local_model_path == "/path/to/mymodel"


def test_check_and_convert_options(mock_model):
    options = {"option1": "5", "option2": "test", "options3": "extra"}
    converted_options = mock_model._check_and_convert_options(**options)
    assert converted_options["option1"] == 5
    assert converted_options["option2"] == "test"
    assert "options3" not in converted_options  # Extra options should be ignored
    assert len(converted_options) == 2  # Only valid options should be included


def test_check_and_convert_options_invalid_type(mock_model):
    options = {"option1": "apple", "option2": "test"}
    with pytest.raises(ValueError):
        mock_model._check_and_convert_options(**options)


def test_embed(mock_model, mocker):
    spy = mocker.spy(mock_model, "_embed_one_batch")
    embedding = mock_model.embed("flying cat")
    assert all(isinstance(x, float) for x in embedding)
    assert len(embedding) == 10
    spy.assert_called_once_with(["flying cat"])


def test_embed_multimodal(mock_multimodal_model, mocker):
    spy = mocker.spy(mock_multimodal_model, "_embed_one_batch_multimodal")

    # Test embedding with default modality (TEXT)
    embedding = mock_multimodal_model.embed("flying cat")
    assert all(isinstance(x, float) for x in embedding)
    spy.assert_called_once_with(["flying cat"], modality=Modality.TEXT)

    # Test embedding with IMAGE modality
    embedding = mock_multimodal_model.embed_image("path/to/image.jpg")
    assert all(isinstance(x, float) for x in embedding)
    spy.assert_called_with(["path/to/image.jpg"], modality=Modality.IMAGE)


def test_embed_model_options(mock_model, mocker):
    options = {"option1": "42", "option2": "test"}
    spy = mocker.spy(mock_model, "_embed_one_batch")
    embedding = mock_model.embed("flying cat", **options)
    assert len(embedding) == 10
    spy.assert_called_once_with(["flying cat"], option1=42, option2="test")


def test_embed_model_options_multimodal(mock_multimodal_model, mocker):
    options = {"option1": "42", "option2": "test"}
    spy = mocker.spy(mock_multimodal_model, "_embed_one_batch_multimodal")

    # Test embedding with default modality (TEXT)
    embedding = mock_multimodal_model.embed("flying cat", **options)
    assert len(embedding) == 10
    spy.assert_called_once_with(["flying cat"], Modality.TEXT, option1=42, option2="test")

    # Test embedding with IMAGE modality
    embedding = mock_multimodal_model.embed_image("path/to/image.jpg", **options)
    assert len(embedding) == 10
    spy.assert_called_with(["path/to/image.jpg"], Modality.IMAGE, option1=42, option2="test")


def test_embed_batch(mock_model, mocker):
    inputs = ["input1", "input2", "input3", "input4", "input5"]
    spy = mocker.spy(mock_model, "_embed_one_batch")
    embeddings = list(mock_model.embed_batch(inputs, None))
    assert len(embeddings) == len(inputs)
    assert spy.call_count == 3  # 2 full batches and 1 partial batch
    spy.assert_has_calls([mocker.call(inputs[:2]), mocker.call(inputs[2:4]), mocker.call(inputs[4:])])


def test_embed_batch_multimodal(mock_multimodal_model, mocker):
    spy = mocker.spy(mock_multimodal_model, "_embed_one_batch_multimodal")

    # Test embedding with default modality (TEXT)
    inputs = ["input1", "input2", "input3", "input4", "input5"]
    embeddings = list(mock_multimodal_model.embed_batch(inputs, None))
    assert len(embeddings) == len(inputs)
    spy.assert_has_calls(
        [
            mocker.call(inputs[:2], Modality.TEXT),
            mocker.call(inputs[2:4], Modality.TEXT),
            mocker.call(inputs[4:], Modality.TEXT),
        ]
    )

    # Test embedding with IMAGE modality
    inputs = ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg", "image5.jpg"]
    embeddings = list(mock_multimodal_model.embed_image_batch(inputs, None))
    assert len(embeddings) == len(inputs)
    spy.assert_has_calls(
        [
            mocker.call(inputs[:2], Modality.IMAGE),
            mocker.call(inputs[2:4], Modality.IMAGE),
            mocker.call(inputs[4:], Modality.IMAGE),
        ]
    )


def test_embed_batch_model_options(mock_model, mocker):
    inputs = ["input1", "input2", "input3", "input4", "input5"]
    options = {"option1": "42", "option2": "test"}
    spy = mocker.spy(mock_model, "_embed_one_batch")
    embeddings = list(mock_model.embed_batch(inputs, None, **options))
    assert len(embeddings) == len(inputs)
    assert spy.call_count == 3  # 2 full batches and 1 partial batch
    spy.assert_has_calls(
        [
            mocker.call(inputs[:2], option1=42, option2="test"),
            mocker.call(inputs[2:4], option1=42, option2="test"),
            mocker.call(inputs[4:], option1=42, option2="test"),
        ]
    )


def test_embed_batch_model_options_multimodal(mock_multimodal_model, mocker):
    options = {"option1": "42", "option2": "test"}
    spy = mocker.spy(mock_multimodal_model, "_embed_one_batch_multimodal")

    # Test embedding with default modality (TEXT)
    inputs = ["input1", "input2", "input3", "input4", "input5"]
    embeddings = list(mock_multimodal_model.embed_batch(inputs, None, **options))
    assert len(embeddings) == len(inputs)
    spy.assert_has_calls(
        [
            mocker.call(inputs[:2], Modality.TEXT, option1=42, option2="test"),
            mocker.call(inputs[2:4], Modality.TEXT, option1=42, option2="test"),
            mocker.call(inputs[4:], Modality.TEXT, option1=42, option2="test"),
        ]
    )

    # Test embedding with IMAGE modality
    inputs = ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg", "image5.jpg"]
    embeddings = list(mock_multimodal_model.embed_image_batch(inputs, None, **options))
    assert len(embeddings) == len(inputs)
    spy.assert_has_calls(
        [
            mocker.call(inputs[:2], Modality.IMAGE, option1=42, option2="test"),
            mocker.call(inputs[2:4], Modality.IMAGE, option1=42, option2="test"),
            mocker.call(inputs[4:], Modality.IMAGE, option1=42, option2="test"),
        ]
    )


def test_embed_batch_custom_batch_size(mock_model, mocker):
    inputs = ["input1", "input2", "input3", "input4", "input5", "input6", "input7", "input8", "input9", "input10"]
    spy = mocker.spy(mock_model, "_embed_one_batch")
    batch_size = 3
    embeddings = list(mock_model.embed_batch(inputs, batch_size))
    assert len(embeddings) == len(inputs)
    assert spy.call_count == 4  # 3 full batches and 1 partial batch
    spy.assert_has_calls(
        [mocker.call(inputs[:3]), mocker.call(inputs[3:6]), mocker.call(inputs[6:9]), mocker.call(inputs[9:])]
    )


def test_embed_batch_custom_batch_size_model_options(mock_model, mocker):
    inputs = ["input1", "input2", "input3", "input4", "input5", "input6", "input7", "input8", "input9", "input10"]
    options = {"option1": "42", "option2": "test"}
    batch_size = 3
    spy = mocker.spy(mock_model, "_embed_one_batch")
    embeddings = list(mock_model.embed_batch(inputs, batch_size, **options))
    assert len(embeddings) == len(inputs)
    assert spy.call_count == 4  # 3 full batches and 1 partial batch
    spy.assert_has_calls(
        [
            mocker.call(inputs[:3], option1=42, option2="test"),
            mocker.call(inputs[3:6], option1=42, option2="test"),
            mocker.call(inputs[6:9], option1=42, option2="test"),
            mocker.call(inputs[9:], option1=42, option2="test"),
        ]
    )


def test_register(mocker):
    mock_model_cls = mocker.Mock()  # Mocking the model class
    mock_model_cls.vendor = "mock"
    mock_model_cls.model_aliases = [("text-emb-1", ["textemb1", "emb1"]), ("text-emb-2", ["textemb2", "emb2"])]
    mock_model_instance = mocker.Mock()  # Mocking the model instance
    mock_factory = mocker.Mock()  # Mocking the factory function
    mock_factory.return_value = mock_model_instance

    register(mock_model_cls, mock_factory)

    assert mock_model_cls in avaliable_models()
    assert get_model("text-emb-1") == mock_model_instance
    assert get_model("textemb1") == mock_model_instance
    assert get_model("emb1") == mock_model_instance
    assert get_model("text-emb-2") == mock_model_instance
    assert get_model("textemb2") == mock_model_instance
    assert get_model("emb2") == mock_model_instance


def test_get_model(plugin_manager):
    model = get_model("mock1")
    assert model is not None
    assert isinstance(model, EmbeddingModel)
    assert model.vendor == "mock"
    assert model.model_id == "embedding-mock-1"

    local_model = get_model("local-mock/mymodel")
    assert local_model is not None
    assert isinstance(local_model, LocalEmbeddingModel)
    assert local_model.vendor == "mock-local"
    assert local_model.model_id == "local-embedding-mock"
    assert local_model.local_model_id == "mymodel"

    local_model_path = get_model("local-mock", model_path="/path/to/mymodel")
    assert local_model_path is not None
    assert isinstance(local_model_path, LocalEmbeddingModel)
    assert local_model_path.vendor == "mock-local"
    assert local_model_path.model_id == "local-embedding-mock"
    assert local_model_path.local_model_path == "/path/to/mymodel"

    mm_model = get_model("mm-mock1")
    assert mm_model is not None
    assert isinstance(mm_model, MultimodalEmbeddingModel)
    assert mm_model.vendor == "mock-multimodal"
    assert mm_model.model_id == "multimodal-mock-1"

    local_mm_model = get_model("local-mm-mock/mymodel")
    assert local_mm_model is not None
    assert isinstance(local_mm_model, LocalMultimodalEmbeddingModel)
    assert local_mm_model.vendor == "mock-local-multimodal"
    assert local_mm_model.model_id == "local-multimodal-embedding-mock"
    assert local_mm_model.local_model_id == "mymodel"

    local_mm_model_path = get_model("local-mm-mock", model_path="/path/to/mymodel")
    assert local_mm_model_path is not None
    assert isinstance(local_mm_model_path, LocalMultimodalEmbeddingModel)
    assert local_mm_model_path.vendor == "mock-local-multimodal"
    assert local_mm_model_path.model_id == "local-multimodal-embedding-mock"
    assert local_mm_model_path.local_model_path == "/path/to/mymodel"
