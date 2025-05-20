import json
import os

import pytest
from click.testing import CliRunner
from embcli_core.cli import embed

skip_if_no_envvar_to_run = pytest.mark.skipif(
    not os.environ.get("RUN_LLAMACPP_TESTS") == "1",
    reason="RUN_LLAMACPP_TESTS environment variable not set",
)


@skip_if_no_envvar_to_run
def test_embed_command(plugin_manager, test_model_file, mocker):
    mocker.patch("embcli_core.cli._pm", plugin_manager)
    runner = CliRunner()
    result = runner.invoke(embed, ["--model", "llama-cpp", "--model-path", test_model_file, "flying cat"])
    assert result.exit_code == 0

    embeddings = json.loads(result.output)
    assert isinstance(embeddings, list)
    assert all(isinstance(val, float) for val in embeddings)
