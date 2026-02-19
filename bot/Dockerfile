FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock* ./

# Устанавливаем Poetry и зависимости
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY . .

RUN mkdir -p /app/logs && chown -R appuser:appuser /app

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app

# Запускаем бота
CMD ["python", "-m", "main"]