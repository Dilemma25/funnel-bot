# ========== BUILDER STAGE ==========
FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --no-interaction --no-ansi

# ========== RUNTIME STAGE ==========
FROM python:3.12-slim AS runtime

WORKDIR /app

RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=builder /app/.venv /app/.venv

COPY . .

RUN mkdir -p /app/logs \
    && chown -R appuser:appuser /app/logs \
    && chmod -R 775 /app/logs

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

USER appuser

CMD ["uvicorn", "src.webhooks.funnel_bot_server.app:app","--host", "0.0.0.0","--port", "8000","--lifespan", "on","--proxy-headers"]