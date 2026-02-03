FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && poetry install --no-root

COPY . .

RUN mkdir -p /app/var/log

ENV PYTHONPATH=/app

CMD ["sh", "-c", "poetry run arq src.processing.workers.user_worker.worker_settings.WorkerSettings >> /app/var/log/consumer.log 2>&1"]