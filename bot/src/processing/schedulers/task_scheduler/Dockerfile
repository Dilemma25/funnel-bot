FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && poetry install --no-root

RUN mkdir -p /app/logs

COPY . .

RUN chmod +x /app/scripts/task_scheduler/entrypoint.sh && \
    crontab /app/scripts/task_scheduler/crontab

ENV PYTHONPATH=/app

ENTRYPOINT ["sh", "/app/scripts/task_scheduler/entrypoint.sh"]