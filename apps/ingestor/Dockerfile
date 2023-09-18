FROM python:3.10

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]