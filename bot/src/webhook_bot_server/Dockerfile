FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .

RUN mkdir -p /app/logs

ENV PYTHONPATH=/app

CMD ["python", "-m", "src.webhook_bot_server"]