FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY apps/ingestor/ingestor ingestor
COPY common/models models

CMD ["uvicorn", "ingestor.main:app", "--host", "0.0.0.0", "--port", "8000"]
