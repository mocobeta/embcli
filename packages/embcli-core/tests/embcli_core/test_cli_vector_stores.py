from click.testing import CliRunner
from embcli_core.cli import vector_stores


def test_vector_stores_command(plugin_manager, mocker):
    """Test the vector stores command."""
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(vector_stores)

    # Check if the command runs successfully
    assert result.exit_code == 0

    # Check if the output contains the expected vector store names
    assert "MockVectorStore" in result.output
    assert "Vendor: mock" in result.output
