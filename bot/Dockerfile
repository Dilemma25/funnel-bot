FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock* ./

# Устанавливаем Poetry и зависимости
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

RUN groupadd -r -g 1000 appuser && useradd -r -u 1000 -g appuser appuser

RUN mkdir -p /app/logs && \
    chown -R appuser:appuser /app

COPY --chown=appuser:appuser . .

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app

# Запускаем бота
CMD ["python", "-m", "main"]