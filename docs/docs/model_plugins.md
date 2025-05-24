# Model Plugins

A model plugin is a Python package for a specific embedding model or model vendor. All model plugins contain the same set of commands, and multiple model plugins can be simultaneously installed in the same environment.

## Proprietary Models

### OpenAI Models

The [embcli-openai](https://pypi.org/project/embcli-openai/) plugin provides access to [OpenAI's embedding models](https://platform.openai.com/docs/models).

You need an OpenAI API key to use this plugin. Set the `OPENAI_API_KEY` environment variable in a `.env` file in the current directory, or specify the path to the env file using the `-e` option.

```bash
cat .env
OPENAI_API_KEY=<YOUR_OPENAI_KEY>
```

**Installation:** `pip install embcli-openai`

`emb models` command shows the available models with there short aliases and supported model options.

```bash
emb models
OpenAIEmbeddingModel
    Vendor: openai
    Models:
    * text-embedding-3-small (aliases: 3-small)
    * text-embedding-3-large (aliases: 3-large)
    * text-embedding-ada-002 (aliases: ada-002)
    Model Options:
    * dimensions (int) - The number of dimensions the resulting output embeddings should have. Only supported in text-embedding-3 and later models.
```

**Example usage:** get an embedding for an input text by text-embedding-3-small model with an option dimensions=512.

```bash
emb embed -m 3-small -o dimensions 512 \
"Owls can rotate their necks 270 degrees without injury🦉"
```

### Cohere Models

The [embcli-cohere](https://pypi.org/project/embcli-cohere/) plugin provides access to [Cohere's embedding models](https://docs.cohere.com/v2/docs/cohere-embed).

You need a Cohere API key to use this plugin. Set the `COHERE_API_KEY` environment variable in a `.env` file in the current directory, or specify the path to the env file using the `-e` option.

```bash
cat .env
COHERE_API_KEY=<YOUR_COHERE_KEY>
```

**Installation:** `pip install embcli-cohere`

`emb models` command shows the available models with there short aliases and supported model options.

```bash
emb models
CohereEmbeddingModel
    Vendor: cohere
    Models:
    * embed-v4.0 (aliases: embed-v4)
    * embed-english-v3.0 (aliases: embed-en-v3)
    * embed-english-light-v3.0 (aliases: embed-en-light-v3)
    * embed-multilingual-v3.0 (aliases: embed-multiling-v3)
    * embed-multilingual-light-v3.0 (aliases: embed-multiling-light-v3)
    Model Options:
    * input_type (str) - The type of input, affecting how the model processes it. Options include 'search_document', 'search_query', 'classification', 'clustering', 'image'.
    * truncate (str) - How to handle text inputs that exceed the model's token limit. Options include 'none', 'start', 'end', 'middle'.
```

**Example usage:** get an embedding for an input text by embed-v4.0 model with an option input_type=search_query.

```bash
emb embed -m embed-v4 -o input_type search_query \
"Owls can rotate their necks 270 degrees without injury🦉"
```

### Gemini Models

The [embcli-gemini](https://pypi.org/project/embcli-gemini/) plugin provides access to [Gemini's embedding models](https://ai.google.dev/gemini-api/docs/models#text-embedding).

You need a Gemini API key to use this plugin. Set the `GEMINI_API_KEY` environment variable in a `.env` file in the current directory, or specify the path to the env file using the `-e` option.

```bash
cat .env
GEMINI_API_KEY=<YOUR_GEMINI_KEY>
```

**Installation:** `pip install embcli-gemini`

`emb models` command shows the available models with there short aliases and supported model options.

```bash
GeminiEmbeddingModel
    Vendor: gemini
    Models:
    * gemini-embedding-exp-03-07 (aliases: exp-03-07)
    * text-embedding-004 (aliases: text-004)
    * embedding-001 (aliases: )
    Model Options:
    * task_type (str) - The type of task for the embedding. Supported task types: 'semantic_similarity', 'classification', 'clustering', 'retrieval_document', 'retrieval_query', 'question_answering', 'fact_verification', 'code_retrieval_query'
```

**Example usage:** get an embedding for an input text by text-embedding-004 model with an option task_type=classification.

```bash
emb embed -m text-004 -o task_type classification \
"Owls can rotate their necks 270 degrees without injury🦉"
```

### Jina Models

The [embcli-jina](https://pypi.org/project/embcli-jina/) plugin provides access to [Jina's embedding models](https://jina.ai/models).

You need a Jina API key to use this plugin. Set the `JINA_API_KEY` environment variable in a `.env` file in the current directory, or specify the path to the env file using the `-e` option.

```bash
cat .env
JINA_API_KEY=<YOUR_JINA_KEY>
```

**Installation:** `pip install embcli-jina`

`emb models` command shows the available models with their short aliases and supported model options.

```bash
emb models
JinaEmbeddingModel
    Vendor: jina
    Models:
    * jina-embeddings-v3 (aliases: jina-v3)
    * jina-colbert-v2 (aliases: colbert-v2)
    * jina-embeddings-v2-base-code (aliases: jina-v2-code)
    Model Options:
    * task (str) - Downstream task for which the embeddings are used. Supported tasks: 'text-matching', 'retrieval.query', 'retrieval.passage', 'separation', 'classification'. Only supported in jina-embeddings-v3.
    * late_chunking (bool) - Whether if the late chunking is applied. Only supported in jina-embeddings-v3.
    * truncate (bool) - When enabled, the model will automatically drop the tail that extends beyond the maximum context length allowed by the model instead of throwing an error. Only supported in jina-embeddings-v3.
    * dimensions (int) - The number of dimensions the resulting output embeddings should have. Only supported in jina-embeddings-v3 and jina-colbert-v2.
    * input_type (str) - The type of input to the model. Supported types: 'query', 'document' Only supported in jina-corebert-v2.
```

**Example usage:** get an embedding for an input text by jina-embeddings-v3 model model with an option dimensions=512.

```bash
emb embed -m jina-v3 -o dimensions 512 \
"Owls can rotate their necks 270 degrees without injury🦉"
```

### Mistral Models

The [embcli-mistral](https://pypi.org/project/embcli-mistral/) plugin provides access to [Mistral's embedding models](https://docs.mistral.ai/capabilities/embeddings/).

You need a Mistral API key to use this plugin. Set the `MISTRAL_API_KEY` environment variable in a `.env` file in the current directory, or specify the path to the env file using the `-e` option.

```bash
cat .env
MISTRAL_API_KEY=<YOUR_MISTRAL_KEY>
```

**Installation:** `pip install embcli-mistral`

`emb models` command shows the available models with their short aliases and supported model options.

```bash
emb models
MistralEmbeddingModel
    Vendor: mistral
    Models:
    * mistral-embed (aliases: )
    Model Options:
```

**Example usage:** get an embedding for an input text by mistral-embed model.

```bash
emb embed -m mistral-embed \
"Owls can rotate their necks 270 degrees without injury🦉"
```

### VoyageAI Models

The [embcli-voyage](https://pypi.org/project/embcli-voyage/) plugin provides access to [VoyageAI's embedding models](https://docs.voyageai.com/docs/embeddings).

You need a VoyageAI API key to use this plugin. Set the `VOYAGE_API_KEY` environment variable in a `.env` file in the current directory, or specify the path to the env file using the `-e` option.

```bash
cat .env
VOYAGE_API_KEY=<YOUR_VOYAGE_KEY>
```

**Installation:** `pip install embcli-voyage`

`emb models` command shows the available models with their short aliases and supported model options.

```bash
emb models
VoyageEmbeddingModel
    Vendor: voyage
    Models:
    * voyage-3-large (aliases: )
    * voyage-3 (aliases: )
    * voyage-3-lite (aliases: )
    * voyage-code-3 (aliases: )
    * voyage-finance-2 (aliases: )
    * voyage-law-2 (aliases: )
    * voyage-code-2 (aliases: )
    Model Options:
    * input_type (str) - Type of the input text. Options: 'None', 'query', 'document' Defaults to 'None'.
    * truncation (bool) - Whether to truncate the input texts to fit within the context length. Defaults to True.
    * output_dimension (int) - The number of dimensions for resulting output embeddings.
```

**Example usage:** get an embedding for an input text by voyage-3-large model with options input_type=query and dimensions=512.

```bash
emb embed -m voyage-3-large -o input_type query -o output_dimension 512 \
"Owls can rotate their necks 270 degrees without injury🦉"
```

## Open Source Models / Local Models

### Sentence Transformers (SBERT) Models

The [embcli-sbert](https://pypi.org/project/embcli-sbert/) plugin provides access to [Sentence Transformers](https://www.sbert.net/) models.

**Installation:** `pip install embcli-sbert`

`emb models` command shows the available models with their short aliases and supported model options.

```bash
emb models
SentenceTransformerModel
    Vendor: sbert
    Models:
    * sentence-transformers (aliases: sbert)
    See https://sbert.net/docs/sentence_transformer/pretrained_models.html for available models.
    Model Options:
```

**Example usage:** get an embedding for an input text by an original sentence-transformers model (e.g. all-MiniLM-L6-v2) or a community model.
Unlike proprietary models, you need to add `sbert/` to the model prefix.

```bash
# Use an original sentence-transformers model
emb embed -m sbert/all-MiniLM-L6-v2 
"Owls can rotate their necks 270 degrees without injury🦉"

# Use a community model
emb embed -m sbert/intfloat/multilingual-e5-small \
"Owls can rotate their necks 270 degrees without injury🦉"
```

### llama.cpp Models

The [embcli-llamacpp](https://pypi.org/project/embcli-llamacpp/) plugin provides access to locally installed models via [llama.cpp](https://github.com/ggml-org/llama.cpp) and [llama-cpp-python](https://github.com/abetlen/llama-cpp-python).

You need to have `gguf` model files in your local machine. See [this tutorial](https://github.com/ggml-org/llama.cpp/discussions/7712) for instructions on how to convert original Hugging Face transformer models to `gguf` format.

**Installation:** `pip install embcli-llamacpp`

`emb models` command shows the available models with their short aliases and supported model options.

```bash
LlamaCppModel
    Vendor: llama-cpp
    Models:
    * llama-cpp (aliases: llamacpp)
    Model Options:
```

**Example usage:** get an embedding for an input text by running the GGUF converted model.

```bash
# Assume you have a GGUF converted all-MiniLM-L6-v2 model in the current directory.
emb embed -m llamacpp -p ./all-MiniLM-L6-v2.F16.gguf \
"Owls can rotate their necks 270 degrees without injury🦉"
```