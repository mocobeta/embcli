import pytest
from embcli_clip import clip
from embcli_clip.clip import CLIPModel


@pytest.fixture
def clip_model():
    return CLIPModel("clip", local_model_id="openai/clip-vit-base-patch32")


@pytest.fixture
def plugin_manager():
    """Fixture to provide a pluggy plugin manager."""
    import pluggy
    from embcli_core import hookspecs

    pm = pluggy.PluginManager("embcli")
    pm.add_hookspecs(hookspecs)
    pm.register(clip)
    return pm
