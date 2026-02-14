FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock* ./

# Устанавливаем Poetry и зависимости
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Копируем весь код
COPY . .

# Создаем директорию для логов
RUN mkdir -p /app/logs

# Устанавливаем PYTHONPATH
ENV PYTHONPATH=/app

# Запускаем бота
CMD ["python", "-m", "main"]