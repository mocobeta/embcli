from click.testing import CliRunner
from embcli_core.cli import simscore


def test_simscore_command_with_texts(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(simscore, ["--model", "embedding-mock-1", "flying cat", "sleepy kitten"])
    assert result.exit_code == 0

    score = float(result.output.strip())
    assert isinstance(score, float)
    assert float(result.output.strip())


def test_simscore_command_with_files(plugin_manager, mocker, tmp_path):
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    # Create a temporary files with test content
    test_file1 = tmp_path / "test_file.txt"
    test_file1.write_text("This is a test text from a file")
    test_file2 = tmp_path / "test_file2.txt"
    test_file2.write_text("This is another test text from a file")

    runner = CliRunner()
    result = runner.invoke(
        simscore, ["--model", "embedding-mock-1", "--file1", str(test_file1), "--file2", str(test_file2)]
    )
    assert result.exit_code == 0

    score = float(result.output.strip())
    assert isinstance(score, float)


def test_simscore_command_with_images(plugin_manager, mocker, tmp_path):
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    # Create a temporary image files
    test_image1 = tmp_path / "test_image1.jpg"
    test_image1.write_bytes(b"This is a test image content")
    test_image2 = tmp_path / "test_image2.jpg"
    test_image2.write_bytes(b"This is another test image content")

    runner = CliRunner()
    result = runner.invoke(
        simscore, ["--model", "multimodal-mock-1", "--image1", str(test_image1), "--image2", str(test_image2)]
    )
    assert result.exit_code == 0

    score = float(result.output.strip())
    assert isinstance(score, float)


def test_simscore_command_with_mixed_inputs(plugin_manager, mocker, tmp_path):
    mocker.patch("embcli_core.cli._pm", plugin_manager)

    # Create a temporary text file
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("This is a test text from a file")
    # Create a temporary image file
    test_image = tmp_path / "test_image.jpg"
    test_image.write_bytes(b"This is a test image content")

    runner = CliRunner()
    result = runner.invoke(
        simscore, ["--model", "multimodal-mock-1", "--file1", str(test_file), "--image2", str(test_image)]
    )
    assert result.exit_code == 0

    score = float(result.output.strip())
    assert isinstance(score, float)

    result = runner.invoke(
        simscore, ["--model", "multimodal-mock-1", "--image1", str(test_image), "--file2", str(test_file)]
    )
    assert result.exit_code == 0
    score = float(result.output.strip())
    assert isinstance(score, float)


def test_simscore_command_with_similarity_option(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()

    # Test with dot product
    mocker.patch("embcli_core.similarities.dot_product", return_value=0.9)
    result_dot = runner.invoke(simscore, ["--model", "mock1", "--similarity", "dot", "Text one", "Text two"])
    assert result_dot.exit_code == 0
    assert float(result_dot.output.strip()) == 0.9

    # Test with cosine similarity
    mocker.patch("embcli_core.similarities.cosine_similarity", return_value=0.8)
    result_cosine = runner.invoke(simscore, ["--model", "mock1", "--similarity", "cosine", "Text one", "Text two"])
    assert result_cosine.exit_code == 0
    assert float(result_cosine.output.strip()) == 0.8

    # Test with euclidean distance
    mocker.patch("embcli_core.similarities.euclidean_distance", return_value=0.7)
    result_euclidean = runner.invoke(
        simscore, ["--model", "mock1", "--similarity", "euclidean", "Text one", "Text two"]
    )
    assert result_euclidean.exit_code == 0
    assert float(result_euclidean.output.strip()) == 0.7

    # Test with manhattan distance
    mocker.patch("embcli_core.similarities.manhattan_distance", return_value=0.6)
    result_manhattan = runner.invoke(
        simscore, ["--model", "mock1", "--similarity", "manhattan", "Text one", "Text two"]
    )
    assert result_manhattan.exit_code == 0
    assert float(result_manhattan.output.strip()) == 0.6


def test_simscore_command_no_input():
    """Test error handling when no text or file is provided."""
    runner = CliRunner()
    result = runner.invoke(simscore, ["--model", "mock1"])

    assert "Error: Please provide either two texts or two files to compare." in result.output


def test_simscore_command_local_model(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(simscore, ["--model", "local-mock/mymodel", "flying cat", "sleepy kitten"])
    assert result.exit_code == 0

    score = float(result.output.strip())
    assert isinstance(score, float)
    assert float(result.output.strip())


def test_simscore_command_local_model_path(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(
        simscore, ["--model", "local-mock", "--model-path", "/path/to/mymodel", "flying cat", "sleepy kitten"]
    )
    assert result.exit_code == 0

    score = float(result.output.strip())
    assert isinstance(score, float)
    assert float(result.output.strip())


def simscore_command_unknown_model(plugin_manager, mocker):
    """Test error handling when an unknown model is provided."""
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(simscore, ["--model", "xyz", "flying cat", "sleepy kitten"])

    assert result.exit_code != 0
    assert "Error: Unknown model id or alias 'xyz'." in result.output
