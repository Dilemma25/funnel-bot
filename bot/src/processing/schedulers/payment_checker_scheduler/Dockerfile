FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry && poetry install --no-root

RUN mkdir -p /app/logs

COPY . .

ENV PYTHONPATH=/app

CMD ["poetry", "run", "python", "src/processing/schedulers/payment_checker_scheduler/payment_checker_runner.py"]