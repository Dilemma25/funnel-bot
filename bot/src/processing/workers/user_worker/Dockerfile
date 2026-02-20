FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && poetry install --no-root

RUN mkdir -p /app/logs

COPY . .

ENV PYTHONPATH=/app

CMD ["poetry", "run", "arq", "src.processing.workers.user_worker.worker_settings.WorkerSettings"]