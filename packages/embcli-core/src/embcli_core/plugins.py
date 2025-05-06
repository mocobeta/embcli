import pluggy

from . import hookspecs, models, vector_stores
from .vector_store import chroma


def get_plugin_manager():
    """Get the plugin manager for the embcli package."""
    pm = pluggy.PluginManager("embcli")
    pm.add_hookspecs(hookspecs)
    pm.load_setuptools_entrypoints("embcli")
    pm.register(chroma)
    pm.check_pending()
    return pm


def register_models(pm: pluggy.PluginManager):
    """Register all embedding models with the plugin manager."""
    for model_cls, factory in pm.hook.embedding_model():
        models.register(model_cls, factory)


def register_vector_stores(pm: pluggy.PluginManager):
    """Register all vector stores with the plugin manager."""
    for vector_store_cls, factory in pm.hook.vector_store():
        vector_stores.register(vector_store_cls, factory)
