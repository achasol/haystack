## Haystack RAG poc

Playing around with Haystack.

### Instructions

1. load the virtual env
2. install deps
3. run the bento docker container

Setup a virtual environment

```
venv ./rag-pipeline/env
```

Start the virtual environment (windws specific).

```
./rag-pipeline/env/Scripts/activate
```

Nagivate into the rag-pipeline folder

```
cd rag-pipeline
```

Then install the required dependencies:

```
pip install -r requirements.txt
```

To start the service run:

```
bentoml serve service.py:Basicpipeline
```
