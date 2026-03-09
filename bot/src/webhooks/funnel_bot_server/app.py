from src.core.logging_config import setup_logging
logger = setup_logging(__name__, service="funnel_bot")


from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi import Header
from fastapi import HTTPException

from contextlib import asynccontextmanager
from aiogram.types import Update

from src.core.database import close_db
from src.core.database import init_db
from src.safe_bot import SafeBot
from src.core.config import settings
from src.bootstrap.funnel_bot.setup_dispatcher import setup_dispatcher

from typing import Optional


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    logger.info("🚀 Starting webhook server...")

    # === STARTUP ===
    try:
        # Инициализация БД
        try:
            await init_db()

        except Exception as e:
            logger.error(f"Database connection error : {e}", exc_info=True)

        logger.info("✅ Database initialized")

        # Создание бота
        bot = SafeBot(token=settings.funnel_bot_token, default=DefaultBotProperties(
            protect_content=True,
            parse_mode=ParseMode.MARKDOWN
            )
        )
        fastapi_app.state.bot = bot
        logger.info("✅ Bot initialized")

        # Установка webhook
        webhook_url = f"{settings.funnel_bot_webhook_url}/webhooks/telegram"

        await bot.set_webhook(
            url=webhook_url,
            secret_token=settings.funnel_bot_webhook_secret_token,
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"]
        )

        logger.info(f"✅ Telegram webhook set: {webhook_url}")

        # Создание диспетчера
        fastapi_app.state.dispatcher = setup_dispatcher()
        logger.info("✅ Dispatcher initialized")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise

    yield  # Сервер работает

    # === SHUTDOWN ===
    try:
        logger.info("🛑 Shutting down webhook server...")

        # Удаление webhook
        await bot.delete_webhook(drop_pending_updates=False)
        logger.info("✅ Telegram webhook deleted")

        # Закрытие сессии бота
        await bot.session.close()
        logger.info("✅ Bot session closed")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        await close_db()
        logger.info("✅ Database closed")

# Создание приложения
app = FastAPI(
    title="Funnel Bot Webhook Server",
    description="Telegram webhook сервер для воронки продаж",
    version="1.0.0",
    lifespan=lifespan,
)


# @app.get("/health")
# async def health(request: Request):
#     return {"status": "healthy"}


@app.post("/webhooks/telegram")
async def telegram_webhook(
        request: Request,
        x_telegram_bot_api_secret_token: Optional[str] = Header(None)
):
    try:

        if x_telegram_bot_api_secret_token != settings.funnel_bot_webhook_secret_token:
            logger.warning(
                f"⚠️ Invalid secret token: {x_telegram_bot_api_secret_token}"
            )
            raise HTTPException(status_code=403, detail="Forbidden")

        bot: SafeBot = request.app.state.bot
        dp: Dispatcher = request.app.state.dispatcher

        update_data = await request.json()

        update = Update(**update_data)

        logger.info(f"📩 Received update {update.update_id}")

        await dp.feed_update(bot, update)

        return Response(status_code=200)

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"❌ Error processing webhook: {e}", exc_info=True)
        return Response(status_code=500)