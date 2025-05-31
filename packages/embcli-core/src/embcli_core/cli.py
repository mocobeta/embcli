import json
import os
from importlib import resources
from typing import Optional

import click
import pluggy
from dotenv import load_dotenv

from .document_loader import load_from_csv
from .models import MultimodalEmbeddingModel, avaliable_models, get_model
from .plugins import get_plugin_manager, register_models, register_vector_stores
from .similarities import SimilarityFunction
from .vector_stores import VectorStoreLocalFS, available_vector_stores, get_vector_store

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
        if hasattr(model_cls, "default_local_model"):
            click.echo(f"    Default Local Model: {model_cls.default_local_model}")  # type: ignore
        if hasattr(model_cls, "local_model_list"):
            click.echo(f"    See {model_cls.local_model_list} for available local models.")  # type: ignore
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
@click.option("model_id", "--model", "-m", required=True, help="Model id or alias to use for embedding")
@click.option("--model-path", "-p", required=False, help="Path to the local model")
@click.option("--file", "-f", type=click.Path(exists=True), help="File containing text to embed")
@click.option("image_file", "--image", type=click.Path(exists=True), help="Image file to embed")
@click.option("options", "--option", "-o", type=(str, str), multiple=True, help="key/value options for the model")
@click.argument("text", required=False)
def embed(env_file, model_id, model_path, file, image_file, options, text):
    """Generate embeddings for the provided text or file content."""
    register_models(pm())
    load_env(env_file)

    # Ensure we have either text or file input
    if not text and not file and not image_file:
        click.echo("Error: Please provide either text or a file to embed.", err=True)
        return

    # Initialize the model
    try:
        embedding_model = get_model(model_id, model_path)
        if not embedding_model:
            click.echo(f"Error: Unknown model id or alias '{model_id}'.", err=True)
            return
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        return

    # Convert options to kwargs
    kwargs = dict(options)

    # Generate image embedding if an image file is provided
    if image_file:
        if not isinstance(embedding_model, MultimodalEmbeddingModel):
            click.echo("Error: Image embedding is only supported by multimodal models.", err=True)
            return
        multimodal_embedding_model: MultimodalEmbeddingModel = embedding_model
        try:
            embedding = multimodal_embedding_model.embed_image(image_file, **kwargs)
            output_json = json.dumps(embedding)
            click.echo(output_json)
            return
        except Exception as e:
            click.echo(f"Error generating image embedding: {str(e)}", err=True)
            return

    # Generate text embedding

    if file:
        with open(file, "r", encoding="utf-8") as f:
            input_text = f.read()
    else:
        input_text = text

    try:
        embedding = embedding_model.embed(input_text, **kwargs)
        output_json = json.dumps(embedding)
        click.echo(output_json)
    except Exception as e:
        click.echo(f"Error generating embeddings: {str(e)}", err=True)


@cli.command()
@click.option("--env-file", "-e", default=".env", help="Path to the .env file")
@click.option("model_id", "--model", "-m", required=True, help="Model id or alias to use for embedding")
@click.option("--model-path", "-p", required=False, help="Path to the local model")
@click.option(
    "--similarity",
    "-s",
    default="cosine",
    type=click.Choice(["dot", "cosine", "euclidean", "manhattan"]),
    help="Similarity function to use",
    show_default=True,
)
@click.option("--file1", "-f1", type=click.Path(exists=True), help="First file containing text to compare")
@click.option("--file2", "-f2", type=click.Path(exists=True), help="Second file containing text to compare")
@click.option("image_file1", "--image1", type=click.Path(exists=True), help="First image file to compare")
@click.option("image_file2", "--image2", type=click.Path(exists=True), help="Second image file to compare")
@click.option("options", "--option", "-o", type=(str, str), multiple=True, help="key/value options for the model")
@click.argument("text1", required=False)
@click.argument("text2", required=False)
def simscore(env_file, model_id, model_path, similarity, file1, file2, image_file1, image_file2, options, text1, text2):
    """Calculate similarity score between two inputs."""
    register_models(pm())
    load_env(env_file)

    # Ensure we have either text or file input for both texts
    if (not text1 and not file1 and not image_file1) or (not text2 and not file2 and not image_file2):
        click.echo("Error: Please provide either two texts or two files to compare.", err=True)
        return

    # Initialize the model
    embedding_model = get_model(model_id, model_path)
    if not embedding_model:
        click.echo(f"Error: Unknown model id or alias '{model_id}'.", err=True)
        return

    multimodal_embedding_model: Optional[MultimodalEmbeddingModel] = None
    if image_file1 or image_file2:
        if not isinstance(embedding_model, MultimodalEmbeddingModel):
            click.echo("Error: Image embedding is only supported by multimodal models.", err=True)
            return
        multimodal_embedding_model = embedding_model

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
        # Generate embeddings for both inputs
        if image_file1:
            assert multimodal_embedding_model is not None, "Multimodal model should be initialized for image embedding"
            embedding1 = multimodal_embedding_model.embed_image(image_file1, **kwargs)
        else:
            embedding1 = embedding_model.embed(input_text1, **kwargs)
        if image_file2:
            assert multimodal_embedding_model is not None, "Multimodal model should be initialized for image embedding"
            embedding2 = multimodal_embedding_model.embed_image(image_file2, **kwargs)
        else:
            embedding2 = embedding_model.embed(input_text2, **kwargs)

        # Calculate similarity
        sim_func = SimilarityFunction(similarity).get_similarity_function()
        score = sim_func(embedding1, embedding2)

        click.echo(f"{score}")

    except Exception as e:
        click.echo(f"Error calculating similarity: {str(e)}", err=True)


@cli.command()
@click.option("--env-file", "-e", default=".env", help="Path to the .env file")
@click.option("model_id", "--model", "-m", required=True, help="Model id or alias to use for embedding")
@click.option("--model-path", "-p", required=False, help="Path to the local model")
@click.option(
    "vector_store_vendor",
    "--vector-store",
    default="chroma",
    help="Vector store to use for storing embeddings",
    show_default=True,
)
@click.option("--persist-path", required=False, help="Path to persist the vector store")
@click.option("--collection", "-c", required=True, help="Collection name where to store the embeddings")
@click.option("--file", "-f", required=True, type=click.Path(exists=True), help="File containing text to embed")
@click.option(
    "--input-format", default="csv", type=click.Choice(["csv"]), help="Input format of the file", show_default=True
)
@click.option("--batch-size", default=100, type=int, help="Batch size for embedding", show_default=True)
@click.option("options", "--option", "-o", type=(str, str), multiple=True, help="key/value options for the model")
def ingest(
    env_file,
    model_id,
    model_path,
    vector_store_vendor,
    persist_path,
    collection,
    file,
    input_format,
    batch_size,
    options,
):
    """Ingest documents into the vector store.
    Ingestion-specific embeddings are used if the model provides options for generating search documents-optimized embeddings."""  # noqa: E501
    register_models(pm())
    register_vector_stores(pm())
    load_env(env_file)

    # Initialize the model
    embedding_model = get_model(model_id, model_path)
    if not embedding_model:
        click.echo(f"Error: Unknown model id or alias '{model_id}'.", err=True)
        return

    # Initialize the vector store
    args = {"persist_path": persist_path} if persist_path else {}
    vector_store = get_vector_store(vector_store_vendor, args)
    if not vector_store:
        click.echo(f"Error: Unknown vector store '{vector_store}'.", err=True)
        return

    # Convert options to kwargs
    kwargs = dict(options)

    # Get the data to ingest
    docs = []
    if input_format == "csv":
        docs.extend(load_from_csv(file, **kwargs))
    else:
        click.echo(f"Error: Unsupported input format '{input_format}'.", err=True)
        return

    # Ingest documents into the vector store
    try:
        vector_store.ingest(embedding_model, collection, docs, batch_size, **kwargs)
        click.echo("Documents ingested successfully.")
        click.echo(f"Vector store: {vector_store.vendor} (collection: {collection})")
        if isinstance(vector_store, VectorStoreLocalFS):
            click.echo(f"Persist path: {vector_store.persist_path}")
    except Exception as e:
        click.echo(f"Error ingesting documents: {str(e)}", err=True)


@cli.command()
@click.option("--env-file", "-e", default=".env", help="Path to the .env file")
@click.option("model_id", "--model", "-m", required=True, help="Model id or alias to use for embedding")
@click.option("--model-path", "-p", required=False, help="Path to the local model")
@click.option(
    "vector_store_vendor",
    "--vector-store",
    default="chroma",
    help="Vector store to use for storing embeddings",
    show_default=True,
)
@click.option("--persist-path", required=False, help="Path to persist the vector store")
@click.option("--collection", "-c", required=True, help="Collection name where to store the embeddings")
@click.option(
    "--corpus",
    default="cat-names-en",
    type=click.Choice(
        [
            "cat-names-en",
            "cat-names-ja",
            "dishes-en",
            "dishes-ja",
            "tourist-spots-en",
            "tourist-spots-ja",
            "movies-en",
            "movies-ja",
        ]
    ),
    help="Smaple corpus name to use",
    show_default=True,
)
@click.option("options", "--option", "-o", type=(str, str), multiple=True, help="key/value options for the model")
def ingest_sample(env_file, model_id, model_path, vector_store_vendor, persist_path, collection, corpus, options):
    """Ingest example documents into the vector store."""
    register_models(pm())
    register_vector_stores(pm())
    load_env(env_file)

    # Initialize the model
    embedding_model = get_model(model_id, model_path)
    if not embedding_model:
        click.echo(f"Error: Unknown model id or alias '{model_id}'.", err=True)
        return

    # Initialize the vector store
    args = {"persist_path": persist_path} if persist_path else {}
    vector_store = get_vector_store(vector_store_vendor, args)
    if not vector_store:
        click.echo(f"Error: Unknown vector store '{vector_store}'.", err=True)
        return

    # Convert options to kwargs
    kwargs = dict(options)

    # Get the data to ingest
    docs = []
    file = corpus + ".csv"
    try:
        with resources.path("embcli_core.synth_data", file) as file_path:
            docs.extend(load_from_csv(str(file_path), **kwargs))
    except FileNotFoundError:
        click.echo(f"Error: Corpus '{corpus}' not found.", err=True)
        return

    # Ingest documents into the vector store
    try:
        vector_store.ingest(embedding_model, collection, docs, batch_size=embedding_model.default_batch_size, **kwargs)
        click.echo("Documents ingested successfully.")
        click.echo(f"Vector store: {vector_store.vendor} (collection: {collection})")
        if isinstance(vector_store, VectorStoreLocalFS):
            click.echo(f"Persist path: {vector_store.persist_path}")
    except Exception as e:
        click.echo(f"Error ingesting documents: {str(e)}", err=True)


@cli.command()
@click.option("--env-file", "-e", default=".env", help="Path to the .env file")
@click.option("model_id", "--model", "-m", required=True, help="Model id or alias to use for embedding")
@click.option("--model-path", "-p", required=False, help="Path to the local model")
@click.option(
    "vector_store_vendor",
    "--vector-store",
    default="chroma",
    help="Vector store to use for storing embeddings",
    show_default=True,
)
@click.option("--persist-path", required=False, help="Path to persist the vector store")
@click.option("--collection", "-c", required=True, help="Collection name where the embeddings are stored")
@click.option("--query", "-q", required=True, help="Query text to search for")
@click.option("--top-k", "-k", default=5, type=int, help="Number of top results to return", show_default=True)
@click.option("options", "--option", "-o", type=(str, str), multiple=True, help="key/value options for the model")
def search(env_file, model_id, model_path, vector_store_vendor, persist_path, collection, query, top_k, options):
    """Search for documents in the vector store for the query.
    Query-specific embedding is used if the model provides options for generating search query-optimized embeddings."""  # noqa: E501
    register_models(pm())
    register_vector_stores(pm())
    load_env(env_file)

    # Initialize the model
    embedding_model = get_model(model_id, model_path)
    if not embedding_model:
        click.echo(f"Error: Unknown model id or alias '{model_id}'.", err=True)
        return

    # Initialize the vector store
    args = {"persist_path": persist_path} if persist_path else {}
    vector_store = get_vector_store(vector_store_vendor, args)
    if not vector_store:
        click.echo(f"Error: Unknown vector store '{vector_store_vendor}'.", err=True)
        return

    # Convert options to kwargs
    kwargs = dict(options)

    # Search for documents in the vector store
    try:
        results = vector_store.search(embedding_model, collection, query, top_k, **kwargs)
        click.echo(f"Found {len(results)} results:")
        for hit in results:
            click.echo(f"Score: {hit.score}, Document ID: {hit.doc.id}, Text: {hit.doc.text}")
    except Exception as e:
        click.echo(f"Error searching documents: {str(e)}", err=True)


@cli.command()
@click.option("--env-file", "-e", default=".env", help="Path to the .env file")
@click.option(
    "vector_store_vendor",
    "--vector-store",
    default="chroma",
    help="Vector store to use for storing embeddings",
    show_default=True,
)
@click.option("--persist-path", required=False, help="Path to persist the vector store")
def collections(env_file, vector_store_vendor, persist_path):
    """List collections in the vector store."""
    register_vector_stores(pm())
    load_env(env_file)

    # Initialize the vector store
    args = {"persist_path": persist_path} if persist_path else {}
    vector_store = get_vector_store(vector_store_vendor, args)
    if not vector_store:
        click.echo(f"Error: Unknown vector store '{vector_store_vendor}'.", err=True)
        return

    # List collections in the vector store
    try:
        collections = vector_store.list_collections()
        click.echo("Collections:")
        for collection in collections:
            click.echo(f"- {collection}")
    except Exception as e:
        click.echo(f"Error listing collections: {str(e)}", err=True)


@cli.command()
@click.option("--env-file", "-e", default=".env", help="Path to the .env file")
@click.option(
    "vector_store_vendor",
    "--vector-store",
    default="chroma",
    help="Vector store to use for storing embeddings",
    show_default=True,
)
@click.option("--persist-path", required=False, help="Path to persist the vector store")
@click.option("--collection", "-c", required=True, help="Collection name to delete")
def delete_collection(env_file, vector_store_vendor, persist_path, collection):
    """Delete a collection from the vector store."""
    register_vector_stores(pm())
    load_env(env_file)

    # Initialize the vector store
    args = {"persist_path": persist_path} if persist_path else {}
    vector_store = get_vector_store(vector_store_vendor, args)
    if not vector_store:
        click.echo(f"Error: Unknown vector store '{vector_store_vendor}'.", err=True)
        return

    # Delete the collection from the vector store
    try:
        vector_store.delete_collection(collection)
        click.echo(f"Collection '{collection}' deleted successfully.")
    except Exception as e:
        click.echo(f"Error deleting collection: {str(e)}", err=True)
