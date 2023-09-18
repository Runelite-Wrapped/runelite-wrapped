# Runelite Wrapped Webapp Backend

This is the backend for the Runelite Wrapped Webapp

It is written in python using FastAPI

## Setup

You will need python and a (virtual) environment with the correct dependencies

## Make a python virtual environment

```bash
python3 -m venv venv
. venv/bin/activate
```

## Install the requirements

```bash
pip install -r requirements.txt
```

## Run

### Dev

from the `be` folder with the virtual environment activated run:

```sh
uvicorn src.app:app --reload
```
