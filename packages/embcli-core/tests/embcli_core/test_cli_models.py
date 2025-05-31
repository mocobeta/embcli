from click.testing import CliRunner
from embcli_core.cli import models


def test_models_command(plugin_manager, mocker):
    """Test the models command."""
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(models)

    # Check if the command runs successfully
    assert result.exit_code == 0

    # Check if the output contains the expected model names
    assert "MockEmbeddingModel" in result.output
    assert "Vendor: mock" in result.output
    assert "Models:" in result.output
    assert "embedding-mock-1 (aliases: mock1)" in result.output
    assert "Options:" in result.output
    assert "option1 (int) - Model option 1" in result.output
    assert "option2 (str) - Model option 2" in result.output

    assert "MockLocalEmbeddingModel" in result.output
    assert "Vendor: mock-local" in result.output
    assert "local-embedding-mock (aliases: local-mock)" in result.output
    assert "See https://example.com/models.html" in result.output

    assert "MockMultimodalEmbeddingModel" in result.output
    assert "Vendor: mock-multimodal" in result.output
    assert "multimodal-mock-1 (aliases: mm-mock1)" in result.output
    assert "multimodal-mock-2 (aliases: mm-mock2)" in result.output

    assert "MockLocalMultimodalEmbeddingModel" in result.output
    assert "Vendor: mock-local-multimodal" in result.output
    assert "local-multimodal-embedding-mock (aliases: local-mm-mock)" in result.output
    assert "See https://example.com/models.html" in result.output
