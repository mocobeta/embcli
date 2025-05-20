from click.testing import CliRunner
from embcli_core.cli import ingest, search
from embcli_core.vector_store import chroma


def test_search_command(plugin_manager, mocker, tmp_path, test_csv_file):
    """Test the search command."""
    plugin_manager.register(chroma)
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    test_persist_path = tmp_path / "test_db"
    test_persist_path.mkdir(parents=True, exist_ok=True)

    # Ingest documents into the vector store
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
            str(test_csv_file),
        ],
    )
    assert result.exit_code == 0

    # Search for a query in the vector store
    result = runner.invoke(
        search,
        [
            "--model",
            "embedding-mock-1",
            "--vector-store",
            "chroma",
            "--persist-path",
            str(test_persist_path),
            "--collection",
            "test_collection",
            "--query",
            "which cat is the best for me?",
            "--top-k",
            "3",
        ],
    )
    assert result.exit_code == 0

    # Check if the output contains the expected success message
    assert "Found 3 results" in result.output
    print(result.output)


def test_search_command_local_model(plugin_manager, mocker, tmp_path, test_csv_file):
    """Test the search command."""
    plugin_manager.register(chroma)
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    test_persist_path = tmp_path / "test_db"
    test_persist_path.mkdir(parents=True, exist_ok=True)

    # Ingest documents into the vector store
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
            str(test_csv_file),
        ],
    )
    assert result.exit_code == 0

    # Search for a query in the vector store
    result = runner.invoke(
        search,
        [
            "--model",
            "local-mock/mymodel",
            "--vector-store",
            "chroma",
            "--persist-path",
            str(test_persist_path),
            "--collection",
            "test_collection",
            "--query",
            "which cat is the best for me?",
            "--top-k",
            "3",
        ],
    )
    assert result.exit_code == 0

    # Check if the output contains the expected success message
    assert "Found 3 results" in result.output
    print(result.output)


def test_search_command_local_model_path(plugin_manager, mocker, tmp_path, test_csv_file):
    """Test the search command."""
    plugin_manager.register(chroma)
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    test_persist_path = tmp_path / "test_db"
    test_persist_path.mkdir(parents=True, exist_ok=True)

    # Ingest documents into the vector store
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
            str(test_csv_file),
        ],
    )
    assert result.exit_code == 0

    # Search for a query in the vector store
    result = runner.invoke(
        search,
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
            "--query",
            "which cat is the best for me?",
            "--top-k",
            "3",
        ],
    )
    assert result.exit_code == 0

    # Check if the output contains the expected success message
    assert "Found 3 results" in result.output
    print(result.output)
