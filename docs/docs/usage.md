# Basic Command Usage

We assume you have installed the [embcli-openai](model_plugins.md#openai-models) plugin and have a OpenAI API key to go through this tutorial.

```bash
pip install embcli-openai
```

```bash
cat .env
OPENAI_API_KEY=<YOUR_OPENAI_KEY>
```

## `models` command

`emb models` command lists all available models in the current environment. 

```bash
emb models
```

The output will show the available models in the current environment, including model names, aliases, and supported model options.

```
# Assuming you have installed `embcli-openai` and `embcli-gemini` plugins
OpenAIEmbeddingModel
    Vendor: openai
    Models:
    * text-embedding-3-small (aliases: 3-small)
    * text-embedding-3-large (aliases: 3-large)
    * text-embedding-ada-002 (aliases: ada-002)
    Model Options:
    * dimensions (int) - The number of dimensions the resulting output embeddings should have. Only supported in text-embedding-3 and later models.
GeminiEmbeddingModel
    Vendor: gemini
    Models:
    * gemini-embedding-exp-03-07 (aliases: exp-03-07)
    * text-embedding-004 (aliases: text-004)
    * embedding-001 (aliases: )
    Model Options:
    * task_type (str) - The type of task for the embedding. Supported task types: 'semantic_similarity', 'classification', 'clustering', 'retrieval_document', 'retrieval_query', 'question_answering', 'fact_verification', 'code_retrieval_query'
```

## `embed` command

`emb embed` command generates embeddings for the provided text of file using the specified model.

```bash
emb embed --help
Usage: emb embed [OPTIONS] [TEXT]

  Generate embeddings for the provided text or file content.

Options:
  -e, --env-file TEXT          Path to the .env file
  -m, --model TEXT             Model id or alias to use for embedding
                               [required]
  -f, --file PATH              File containing text to embed
  -o, --option <TEXT TEXT>...  key/value options for the model
  --help                       Show this message and exit.
```

### `--model` option (required)

`--model`/`-m` option specifies the model to use for embedding.

To generate an embedding for an input text by `text-embedding-3-small` model, run this command:

```bash
emb embed -m text-embedding-3-small "Have you taken a coffee break?☕"
```

The output will be a JSON array of floats representing the embedding vector for the input text.
```
[-0.07306485623121262, -0.02141696587204933, -0.021973779425024986, -0.030774157494306564, -0.028927164152264595, -0.020126787945628166, 0.031263068318367004, 0.03911278396844864, -0.025681346654891968, 0.005500235594809055, 0.033544644713401794, -0.011625189334154129, 0.007747862488031387, -0.009350400418043137, ...]
```

You can also use an alias for the model. For example, `text-embedding-3-small` has an alias `3-small`:

```bash
emb embed -m 3-small "Have you taken a coffee break?☕"
```

### `--file` option

To generate an embedding for a text in a file, use the `--file`/`-f` option:

```bash
# Assuming you have a file named `coffee.txt` in the current directory
cat coffee.txt 
How to make a cup of coffee ☕
To boil water, pour it into a kettle or saucepan and heat it on the stove or with an electric kettle. Wait until you see large, steady bubbles rising and breaking on the surface. Once it reaches a rolling boil, the water is ready to use.

emb embed -m 3-small -f coffee.txt
```

### `--option` option

To pass additional options to the model, use the `--option`/`-o` option. The options are model-specific, so please refer [`emb models`](#models-command) command for available options for a specific model.

`OpenAIEmbeddingModel` supports `dimensions` option to specify the number of output dimensions:

```bash
emb embed -m 3-small -o dimensions 512 "Have you taken a coffee break?☕"
```


## `simscore` command

`emb simscore` command calculates the similarity score or distance between two text embeddings.

```bash
emb simscore --help
Usage: emb simscore [OPTIONS] [TEXT1] [TEXT2]

  Calculate similarity score between two texts.

Options:
  -e, --env-file TEXT             Path to the .env file
  -m, --model TEXT                Model id or alias to use for embedding
                                  [required]
  -s, --similarity [dot|cosine|euclidean|manhattan]
                                  Similarity function to use  [default:
                                  cosine]
  -f1, --file1 PATH               First file containing text to compare
  -f2, --file2 PATH               Second file containing text to compare
  -o, --option <TEXT TEXT>...     key/value options for the model
  --help                          Show this message and exit.
```

### `--model` option (required)

`--model`/`-m` option specifies the model to use for embedding.

To calculate the similarity score between two input texts using `text-embedding-3-small` model, run this command:

```bash
emb simscore -m 3-small "I have a cat" "私は猫を飼っています"
```

The output will be a float value calculated by the specified metric (default is cosine similarity):

```
0.5505237095494223
```

### `--similarity` option

`--similarity`/`-s` option specifies the similarity function to use. The available options are `dot`, `cosine`, `euclidean`, and `manhattan`. If two vectors are normalized, `dot` and `cosine` yields the same value. The default is `cosine`.

To calculate the euclidean distance between two input texts, run this command:

```bash
emb simscore -m 3-small -s euclidean "I have a cat" "私は猫を飼っています"
```

### `--file1` and `--file2` options

To calculate the similarity score between two embeddings in files, use the `--file1`/`-f1` and `--file2`/`-f2` options:

```bash
# Assuming you have two files named coffee.txt and caffe.txt in the current directory
cat coffee.txt 
How to make a cup of coffee ☕
To boil water, pour it into a kettle or saucepan and heat it on the stove or with an electric kettle. Wait until you see large, steady bubbles rising and breaking on the surface. Once it reaches a rolling boil, the water is ready to use.

cat caffe.txt 
Come preparare una tazza di caffè ☕
Per far bollire l'acqua, versala in un bollitore o in un pentolino e riscaldala sul fornello o con un bollitore elettrico. Aspetta finché non vedi grandi bolle stabili salire e rompersi sulla superficie. Una volta che l'acqua raggiunge un'ebollizione vigorosa, è pronta per essere usata.

emb simscore -m 3-small -f1 coffee.txt -f2 caffe.txt
```

### `--option` option

To pass additional options to the model, use the `--option`/`-o` option. The options are model-specific, so please refer [`emb models`](#models-command) command for available options for a specific model.


## Common options

Options that are common to all commands.

### `--env` option

`emb` implicitly loads the environment variables from the `.env` file in the current directory. You can also specify a different `.env` file using the `--env`/`-e` option:

```bash
cat /path/to/your/.env
OPENAI_API_KEY=<YOUR_OPENAI_KEY>

emb embed -m 3-small -e /path/to/your/.env "Have you taken a coffee break?☕"
```
