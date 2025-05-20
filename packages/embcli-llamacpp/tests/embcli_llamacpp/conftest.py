from importlib import resources

import pytest
from embcli_llamacpp import llamacpp
from embcli_llamacpp.llamacpp import LlamaCppModel


@pytest.fixture
def test_model_file() -> str:
    file_path = resources.path("tests.embcli_llamacpp.resources", "all-MiniLM-L6-v2.Q3_K_S.gguf")
    return str(file_path)


@pytest.fixture
def llamacpp_model(test_model_file):
    return LlamaCppModel(model_id="llama-cpp", local_model_path=test_model_file)


@pytest.fixture
def plugin_manager():
    import pluggy
    from embcli_core import hookspecs

    pm = pluggy.PluginManager("embcli")
    pm.add_hookspecs(hookspecs)
    pm.register(llamacpp)
    return pm
