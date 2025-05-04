import pluggy

from . import hookspecs, models


def get_plugin_manager():
    """Get the plugin manager for the embcli package."""
    pm = pluggy.PluginManager("embcli")
    pm.add_hookspecs(hookspecs)
    pm.load_setuptools_entrypoints("embcli")
    pm.check_pending()
    return pm


def register_models(pm: pluggy.PluginManager):
    """Register all embedding models with the plugin manager."""
    for model_cls, factory in pm.hook.embedding_model():
        models.register(model_cls, factory)
