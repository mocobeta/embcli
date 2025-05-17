from click.testing import CliRunner
from embcli_core.cli import collections, delete_collection, ingest_sample
from embcli_core.vector_store import chroma


def test_list_delete_collection_command(plugin_manager, mocker, tmp_path):
    plugin_manager.register(chroma)
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    test_persist_path = tmp_path / "test_db"
    test_persist_path.mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    # Create collections with different corpus
    for corpus in ["cat-names-en", "dishes-en", "movies-en"]:
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
                f"test_collection_{corpus}",
                "--corpus",
                corpus,
            ],
        )
        assert result.exit_code == 0
        assert "chroma" in result.output

    # Check if created collections are correctly listed
    result = runner.invoke(
        collections,
        [
            "--vector-store",
            "chroma",
            "--persist-path",
            str(test_persist_path),
        ],
    )
    assert result.exit_code == 0
    assert "test_collection_cat-names-en" in result.output
    assert "test_collection_dishes-en" in result.output
    assert "test_collection_movies-en" in result.output

    # Delete a collection
    result = runner.invoke(
        delete_collection,
        [
            "--vector-store",
            "chroma",
            "--persist-path",
            str(test_persist_path),
            "--collection",
            "test_collection_cat-names-en",
        ],
    )
    assert result.exit_code == 0

    # Check if the collection was deleted
    result = runner.invoke(
        collections,
        [
            "--vector-store",
            "chroma",
            "--persist-path",
            str(test_persist_path),
        ],
    )
    assert result.exit_code == 0
    assert "test_collection_cat-names-en" not in result.output
    assert "test_collection_dishes-en" in result.output
    assert "test_collection_movies-en" in result.output

    # Attempt to delete a non-existing collection
    result = runner.invoke(
        delete_collection,
        [
            "--vector-store",
            "chroma",
            "--persist-path",
            str(test_persist_path),
            "--collection",
            "test_collection_cat-names-en",
        ],
    )
    assert result.exit_code == 0
    assert "Collection [test_collection_cat-names-en] does not exists" in result.output
