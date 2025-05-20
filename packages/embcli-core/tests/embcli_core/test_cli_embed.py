import json

from click.testing import CliRunner
from embcli_core.cli import embed


def test_embed_command_model_id(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "embedding-mock-1", "flying cat"])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 10
    assert all(isinstance(val, float) for val in embeddings)


def test_embed_command_model_id_local(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "local-embedding-mock/mymodel", "flying cat"])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 10
    assert all(isinstance(val, float) for val in embeddings)


def test_embed_command_model_id_local_file(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "local-embedding-mock", "--model-path", "/path/to/mymodel", "flying cat"])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 10
    assert all(isinstance(val, float) for val in embeddings)


def test_embed_command_model_alias(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "mock1", "flying cat"])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 10
    assert all(isinstance(val, float) for val in embeddings)


def test_embed_command_model_alias_local(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "local-mock/mymodel", "flying cat"])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 10
    assert all(isinstance(val, float) for val in embeddings)


def test_embed_command_model_alias_local_file(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "local-mock", "--model-path", "/path/to/mymodel", "flying cat"])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 10
    assert all(isinstance(val, float) for val in embeddings)


def test_embed_command_with_file(plugin_manager, mocker, tmp_path):
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    # Create a temporary file with test content
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("This is a test text from a file")

    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "embedding-mock-1", "--file", str(test_file)])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 10
    assert all(isinstance(val, float) for val in embeddings)


def test_embed_command_with_options(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(
        embed, ["--model", "embedding-mock-1", "--option", "option1", "42", "--option", "option2", "test", "flying cat"]
    )
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 10
    assert all(isinstance(val, float) for val in embeddings)


def test_embed_command_no_input():
    """Test error handling when no text or file is provided."""
    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "mock-001"])
    assert "Error: Please provide either text or a file to embed." in result.output


def test_embed_command_unknown_model(plugin_manager, mocker):
    """Test error handling when an unknown model alias is provided."""
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "xyz", "This is a test text"])

    assert "Error: Unknown model id or alias 'xyz'" in result.output
