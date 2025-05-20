from click.testing import CliRunner
from embcli_core.cli import ingest_sample
from embcli_core.vector_store import chroma


def test_ingest_sample_command(plugin_manager, mocker, tmp_path):
    """Test the ingest command."""
    plugin_manager.register(chroma)
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    test_persist_path = tmp_path / "test_db"
    test_persist_path.mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        ingest_sample,
        [
            "--model",
            "embedding-mock-1",
            "--vector-store",
            "chroma",
            "--persist-path",
            str(test_persist_path),
            "--collection",
            "test_collection",
        ],
    )
    assert result.exit_code == 0

    # Check if the output contains the expected success message
    assert "chroma" in result.output
    assert str(test_persist_path) in result.output

    # Check if the database was created
    assert test_persist_path.exists()


def test_ingest_sample_command_corpus(plugin_manager, mocker, tmp_path):
    """Test the ingest command with corpus."""
    plugin_manager.register(chroma)
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    test_persist_path = tmp_path / "test_db"
    test_persist_path.mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        ingest_sample,
        [
            "--model",
            "embedding-mock-1",
            "--vector-store",
            "chroma",
            "--persist-path",
            str(test_persist_path),
            "--collection",
            "test_collection",
            "--corpus",
            "cat-names-ja",
        ],
    )
    assert result.exit_code == 0

    # Check if the output contains the expected success message
    assert "chroma" in result.output
    assert str(test_persist_path) in result.output

    # Check if the database was created
    assert test_persist_path.exists()


def test_ingest_sample_command_local_model(plugin_manager, mocker, tmp_path):
    """Test the ingest command."""
    plugin_manager.register(chroma)
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    test_persist_path = tmp_path / "test_db"
    test_persist_path.mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        ingest_sample,
        [
            "--model",
            "local-mock/mymodel",
            "--vector-store",
            "chroma",
            "--persist-path",
            str(test_persist_path),
            "--collection",
            "test_collection",
        ],
    )
    assert result.exit_code == 0

    # Check if the output contains the expected success message
    assert "chroma" in result.output
    assert str(test_persist_path) in result.output

    # Check if the database was created
    assert test_persist_path.exists()


def test_ingest_sample_command_local_model_file(plugin_manager, mocker, tmp_path):
    """Test the ingest command."""
    plugin_manager.register(chroma)
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    test_persist_path = tmp_path / "test_db"
    test_persist_path.mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        ingest_sample,
        [
            "--model",
            "local-mock",
            "--model-path",
            "/path/to/mymodel",
            "--vector-store",
            "chroma",
            "--persist-path",
            str(test_persist_path),
            "--collection",
            "test_collection",
        ],
    )
    assert result.exit_code == 0

    # Check if the output contains the expected success message
    assert "chroma" in result.output
    assert str(test_persist_path) in result.output

    # Check if the database was created
    assert test_persist_path.exists()
