## Haystack RAG poc

Playing around with Haystack.

### Instructions

1. load the virtual env
2. install deps
3. run the bento docker container

Start the virtual environment (windws specific).

```
./env/Scripts/activate
```

Then install the required dependencies:

```
pip install -r requirements.txt
```

To start the service run:

```
bentoml serve service.py:Basicpipeline
```
