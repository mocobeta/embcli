from click.testing import CliRunner
from embcli_core.cli import ingest
from embcli_core.vector_store import chroma


def test_ingest_command(plugin_manager, mocker, tmp_path):
    """Test the ingest command."""
    plugin_manager.register(chroma)
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    # Create a temporary file with test content
    test_file = tmp_path / "test_file.csv"
    with test_file.open("w") as f:
        for i in range(10):
            f.write(f"{i},This is a test text\n")

    test_persist_path = tmp_path / "test_db"
    test_persist_path.mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        ingest,
        [
            "--model",
            "embedding-mock-1",
            "--vector-store",
            "chroma",
            "--persist-path",
            str(test_persist_path),
            "--collection",
            "test_collection",
            "--file",
            str(test_file),
        ],
    )
    assert result.exit_code == 0

    # Check if the output contains the expected success message
    assert "chroma" in result.output
    assert str(test_persist_path) in result.output

    # Check if the database was created
    assert test_persist_path.exists()


def test_ingest_command_local_model(plugin_manager, mocker, tmp_path):
    """Test the ingest command."""
    plugin_manager.register(chroma)
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    # Create a temporary file with test content
    test_file = tmp_path / "test_file.csv"
    with test_file.open("w") as f:
        for i in range(10):
            f.write(f"{i},This is a test text\n")

    test_persist_path = tmp_path / "test_db"
    test_persist_path.mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        ingest,
        [
            "--model",
            "local-mock/mymodel",
            "--vector-store",
            "chroma",
            "--persist-path",
            str(test_persist_path),
            "--collection",
            "test_collection",
            "--file",
            str(test_file),
        ],
    )
    assert result.exit_code == 0

    # Check if the output contains the expected success message
    assert "chroma" in result.output
    assert str(test_persist_path) in result.output

    # Check if the database was created
    assert test_persist_path.exists()


def test_ingest_command_local_model_path(plugin_manager, mocker, tmp_path):
    """Test the ingest command."""
    plugin_manager.register(chroma)
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    # Create a temporary file with test content
    test_file = tmp_path / "test_file.csv"
    with test_file.open("w") as f:
        for i in range(10):
            f.write(f"{i},This is a test text\n")

    test_persist_path = tmp_path / "test_db"
    test_persist_path.mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        ingest,
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
            "--file",
            str(test_file),
        ],
    )
    assert result.exit_code == 0

    # Check if the output contains the expected success message
    assert "chroma" in result.output
    assert str(test_persist_path) in result.output

    # Check if the database was created
    assert test_persist_path.exists()
