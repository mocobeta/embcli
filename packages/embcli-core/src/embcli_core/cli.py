import json
import os
from typing import Optional

import click
import pluggy
from dotenv import load_dotenv

from .models import avaliable_models, get_model
from .plugins import get_plugin_manager, register_models, register_vector_stores
from .similarities import SimilarityFunction
from .vector_stores import available_vector_stores

# Placeholder for the plugin manager.
# In production, this will be set to the actual plugin manager.
# In test cases, you would mock this.
_pm: Optional[pluggy.PluginManager] = None


def pm() -> pluggy.PluginManager:
    """Get the plugin manager instance."""
    global _pm
    if _pm is None:
        _pm = get_plugin_manager()
    return _pm


def load_env(env_file):
    """Load environment variables from a .env file."""
    if os.path.exists(env_file):
        load_dotenv(env_file)


@click.group()
def cli():
    pass


@cli.command()
def models():
    """List available models."""
    register_models(pm())

    for model_cls in avaliable_models():
        click.echo(model_cls.__name__)
        click.echo(f"    Vendor: {model_cls.vendor}")
        click.echo("    Models:")
        for model_id, aliases in model_cls.model_aliases:
            click.echo(f"    * {model_id} (aliases: {', '.join(aliases)})")
        click.echo("    Model Options:")
        for option in model_cls.valid_options:
            click.echo(f"    * {option.name} ({option.type.value}) - {option.description}")


@cli.command()
def vector_stores():
    """List available vector stores."""
    register_vector_stores(pm())

    for vector_store_cls in available_vector_stores():
        click.echo(vector_store_cls.__name__)
        click.echo(f"    Vendor: {vector_store_cls.vendor}")


@cli.command()
@click.option("--env-file", "-e", default=".env", help="Path to the .env file")
@click.option("model_id", "--model", "-m", help="Model id or alias to use for embedding")
@click.option("--file", "-f", type=click.Path(exists=True), help="File containing text to embed")
@click.option("options", "--option", "-o", type=(str, str), multiple=True, help="key/value options for the model")
@click.argument("text", required=False)
def embed(env_file, model_id, file, options, text):
    """Generate embeddings for the provided text or file content."""
    register_models(pm())
    load_env(env_file)

    # Ensure we have either text or file input
    if not text and not file:
        click.echo("Error: Please provide either text or a file to embed.", err=True)
        return

    # Initialize the model
    embedding_model = get_model(model_id)
    if not embedding_model:
        click.echo(f"Error: Unknown model id or alias '{model_id}'.", err=True)
        return

    # Convert options to kwargs
    kwargs = dict(options)

    # Get the input text
    if file:
        with open(file, "r", encoding="utf-8") as f:
            input_text = f.read()
    else:
        input_text = text

    # Generate embeddings
    try:
        embeddings = embedding_model.embed(input_text, **kwargs)

        output_json = json.dumps(embeddings)
        click.echo(output_json)
    except Exception as e:
        click.echo(f"Error generating embeddings: {str(e)}", err=True)


@cli.command()
@click.option("--env-file", "-e", default=".env", help="Path to the .env file")
@click.option("model_id", "--model", "-m", help="Model id or alias to use for embedding")
@click.option(
    "--similarity",
    "-s",
    default="cosine",
    type=click.Choice(["dot", "cosine", "euclidean", "manhattan"]),
    help="Similarity function to use",
)
@click.option("--file1", "-f1", type=click.Path(exists=True), help="First file containing text to compare")
@click.option("--file2", "-f2", type=click.Path(exists=True), help="Second file containing text to compare")
@click.option("options", "--option", "-o", type=(str, str), multiple=True, help="key/value options for the model")
@click.argument("text1", required=False)
@click.argument("text2", required=False)
def simscore(env_file, model_id, similarity, file1, file2, options, text1, text2):
    """Calculate similarity score between two texts."""
    register_models(pm())
    load_env(env_file)

    # Ensure we have either text or file input for both texts
    if (not text1 and not file1) or (not text2 and not file2):
        click.echo("Error: Please provide either two texts or two files to compare.", err=True)
        return

    # Initialize the model
    embedding_model = get_model(model_id)
    if not embedding_model:
        click.echo(f"Error: Unknown model id or alias '{model_id}'.", err=True)
        return

    # Convert options to kwargs
    kwargs = dict(options)

    # Get the input texts
    if file1:
        with open(file1, "r", encoding="utf-8") as f:
            input_text1 = f.read()
    else:
        input_text1 = text1

    if file2:
        with open(file2, "r", encoding="utf-8") as f:
            input_text2 = f.read()
    else:
        input_text2 = text2

    try:
        # Generate embeddings for both texts
        embedding1 = embedding_model.embed(input_text1, **kwargs)
        embedding2 = embedding_model.embed(input_text2, **kwargs)

        # Calculate similarity
        sim_func = SimilarityFunction(similarity).get_similarity_function()
        score = sim_func(embedding1, embedding2)

        click.echo(f"{score}")

    except Exception as e:
        click.echo(f"Error calculating similarity: {str(e)}", err=True)
