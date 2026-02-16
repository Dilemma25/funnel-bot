"""
FastAPI webhook сервер для Telegram бота
"""
from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager
from aiogram.types import Update

from src.core.logging_config import setup_logging
from src.core.database import init_db, close_db
from src.safe_bot import SafeBot
from src.core.config import settings
from src.bootstrap.setup_dispatcher import setup_dispatcher

logger = setup_logging(__name__, service="webhook")


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """
    Lifecycle manager

    Startup:
    - Инициализация БД
    - Создание бота
    - Установка webhook в Telegram

    Shutdown:
    - Удаление webhook
    - Закрытие сессии бота
    - Закрытие БД
    """
    logger.info("🚀 Starting webhook server...")

    # === STARTUP ===

    # Инициализация БД
    await init_db()
    logger.info("✅ Database initialized")

    # Создание бота
    bot = SafeBot(settings.bot_token)
    fastapi_app.state.bot = bot
    logger.info("✅ Bot initialized")

    # Установка webhook
    webhook_url = f"{settings.webhook_url}/webhooks/telegram"

    await bot.set_webhook(
        url=webhook_url,
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query"]
    )

    logger.info(f"✅ Telegram webhook set: {webhook_url}")

    # Создание диспетчера
    fastapi_app.state.dispatcher = setup_dispatcher()
    logger.info("✅ Dispatcher initialized")

    yield  # Сервер работает

    # === SHUTDOWN ===

    logger.info("🛑 Shutting down webhook server...")

    # Удаление webhook
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("✅ Telegram webhook deleted")

    # Закрытие сессии бота
    await bot.session.close()
    logger.info("✅ Bot session closed")

    # Закрытие БД
    await close_db()
    logger.info("✅ Database closed")


# Создание приложения
app = FastAPI(
    title="Funnel Bot Webhook Server",
    description="Telegram webhook сервер для воронки продаж",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "ok",
        "service": "funnel-bot-webhook-server",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check для мониторинга"""
    return {"status": "healthy"}


@app.post("/webhooks/telegram")
async def telegram_webhook(request: Request):
    """
    Webhook endpoint для Telegram

    Telegram отправляет сюда все обновления:
    - Новые сообщения
    - Callback query (нажатия на кнопки)
    - И другие события
    """
    try:
        # Получаем бота и диспетчер
        bot = request.app.state.bot
        dp = request.app.state.dispatcher

        # Парсим JSON от Telegram
        update_data = await request.json()

        # Создаём Update объект
        update = Update(**update_data)

        logger.info(f"📩 Received update {update.update_id}")

        # Обрабатываем update через диспетчер
        await dp.feed_update(bot, update)

        return Response(status_code=200)

    except Exception as e:
        logger.error(f"❌ Error processing webhook: {e}", exc_info=True)
        return Response(status_code=500)