#Dockerfile для Scheduler
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && poetry install --no-root

COPY . .

RUN mkdir -p /app/var/log

ENV PYTHONPATH=/app

CMD ["sh", "-c", "echo \"* * * * * cd /app && PYTHONPATH=/app /usr/local/bin/poetry run python src/processing/scheduler_runner.py >> /app/var/log/scheduler.log 2>&1\" | crontab - && cron -f"]