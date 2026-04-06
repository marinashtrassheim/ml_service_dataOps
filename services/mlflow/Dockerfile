FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir mlflow psycopg2-binary

EXPOSE 5000

ENV MLFLOW_BACKEND_STORE_URI=""
ENV MLFLOW_ARTIFACT_ROOT=""

CMD mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --backend-store-uri $MLFLOW_BACKEND_STORE_URI \
    --default-artifact-root $MLFLOW_ARTIFACT_ROOT