FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Установка зависимостей
COPY pyproject.toml poetry.lock* /app/

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем проект
COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.webhook_server.main:app", "--host", "0.0.0.0", "--port", "8000"]