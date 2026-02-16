"""
Точка входа для webhook сервера
Запуск: python -m src.webhook_server
"""
import uvicorn
from src.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.webhook_bot_server.app:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )