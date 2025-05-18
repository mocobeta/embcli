import json
import os

import pytest
from click.testing import CliRunner
from embcli_core.cli import embed

skip_if_no_envvar_to_run = pytest.mark.skipif(
    not os.environ.get("RUN_SBERT_TESTS") == "1",
    reason="RUN_SBERT_TESTS environment variable not set",
)


@skip_if_no_envvar_to_run
def test_embed_command(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "sbert/all-MiniLM-L6-v2", "flying cat"])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 384
    assert all(isinstance(val, float) for val in embeddings)


@skip_if_no_envvar_to_run
def test_embed_command_no_local_model_id(plugin_manager, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "sbert", "flying cat"])
    assert result.exit_code == 0

    assert "model id must contain actual SentenceTransformer model to be used." in result.output
