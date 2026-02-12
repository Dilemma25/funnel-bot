FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && poetry install --no-root

#COPY ../.. .
COPY . .

RUN mkdir -p /app/var/log

ENV PYTHONPATH=/app

CMD ["/bin/sh", "-c", "echo \"* * * * * cd /app && PYTHONPATH=/app /usr/local/bin/poetry run python src/processing/schedulers/task_scheduler/scheduler_runner.py\" | crontab - && cron -f"]
