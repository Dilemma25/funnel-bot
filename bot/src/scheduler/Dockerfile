FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install poetry && poetry install --no-root

RUN mkdir -p /app/var/log

ENV PYTHONPATH=/app

CMD ["sh", "-c", "echo \"* * * * * cd /app && PYTHONPATH=/app /usr/local/bin/poetry run python src/scheduler/runner.py >> /app/var/log/scheduler.log 2>&1\" | crontab - && cron -f"]