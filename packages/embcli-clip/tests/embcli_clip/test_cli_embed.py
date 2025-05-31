import json
import os
from importlib.resources import files

import pytest
from click.testing import CliRunner
from embcli_core.cli import embed

skip_if_no_envvar_to_run = pytest.mark.skipif(
    not os.environ.get("RUN_CLIP_TESTS") == "1",
    reason="RUN_CLIP_TESTS environment variable not set",
)


@skip_if_no_envvar_to_run
def test_embed_command_text(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "clip", "flying cat"])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 512
    assert all(isinstance(val, float) for val in embeddings)


@skip_if_no_envvar_to_run
def test_embed_command_image(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    image_path = files("tests.embcli_clip").joinpath("flying_cat.jpeg")
    result = runner.invoke(embed, ["--model", "clip", "--image", str(image_path)])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 512
    assert all(isinstance(val, float) for val in embeddings)
