FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && poetry install --no-root

RUN groupadd -r -g 1000 appuser && useradd -r -u 1000 -g appuser appuser

RUN mkdir -p /app/logs && \
    chown -R appuser:appuser /app

COPY --chown=appuser:appuser . .

ENV PYTHONPATH=/app

USER appuser

CMD ["poetry", "run", "python", "src/processing/schedulers/payment_checker_scheduler/payment_checker_runner.py"]
