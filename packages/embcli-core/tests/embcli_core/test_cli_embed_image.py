import json

from click.testing import CliRunner
from embcli_core.cli import embed


def test_embed_command_image(plugin_manager, mocker, tmp_path):
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    # Create a temporary image file for testing
    image_path = tmp_path / "flying_cat.jpg"
    with open(image_path, "wb") as f:
        f.write("fake image data for testing".encode())

    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "mm-mock1", "--image", str(image_path)])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 10
    assert all(isinstance(val, float) for val in embeddings)


def test_embed_command_image_local(plugin_manager, mocker, tmp_path):
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    # Create a temporary image file for testing
    image_path = tmp_path / "flying_cat.jpg"
    with open(image_path, "wb") as f:
        f.write("fake image data for testing".encode())

    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "local-mm-mock/mymodel", "--image", str(image_path)])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 10
    assert all(isinstance(val, float) for val in embeddings)


def test_embed_command_image_local_file(plugin_manager, mocker, tmp_path):
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    # Create a temporary image file for testing
    image_path = tmp_path / "flying_cat.jpg"
    with open(image_path, "wb") as f:
        f.write("fake image data for testing".encode())

    runner = CliRunner()
    result = runner.invoke(
        embed, ["--model", "local-mm-mock", "--model-path", "/path/to/mymodel", "--image", str(image_path)]
    )
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 10
    assert all(isinstance(val, float) for val in embeddings)


def test_embed_command_image_with_options(plugin_manager, mocker, tmp_path):
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    # Create a temporary image file for testing
    image_path = tmp_path / "flying_cat.jpg"
    with open(image_path, "wb") as f:
        f.write("fake image data for testing".encode())

    runner = CliRunner()
    result = runner.invoke(
        embed,
        ["--model", "mm-mock1", "--option", "option1", "42", "--option", "option2", "test", "--image", str(image_path)],
    )
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 10
    assert all(isinstance(val, float) for val in embeddings)


def test_embed_command_image_not_supported(plugin_manager, mocker, tmp_path):
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    # Create a temporary image file for testing
    image_path = tmp_path / "flying_cat.jpg"
    with open(image_path, "wb") as f:
        f.write("fake image data for testing".encode())

    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "embedding-mock-1", "--image", str(image_path)])

    # Expecting an error since the model does not support image embedding
    assert "Error: Image embedding is only supported by multimodal models." in result.output
