FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY apps/analytics/analytics analytics
COPY common/models models

CMD ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000", "-m", "analytics"]
