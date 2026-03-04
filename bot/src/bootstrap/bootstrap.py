from src.core.config import settings
from src.core.database import init_db
from src.middlewares.user_check import UserCheckMiddleware
from src.safe_bot import SafeBot
from src.core import init_redis

from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from tortoise import run_async
from .setap_routers import setup_routers
from ..middlewares.error_handler import ErrorHandlerMiddleware
from aiogram.fsm.storage.redis import RedisStorage


async def start_app() -> None:
    run_async(init_db())

    redis = init_redis()
    redis_storage = RedisStorage(redis)

    dispatcher = Dispatcher(storage=redis_storage)

    dispatcher.include_router(setup_routers())

    dispatcher.message.middleware(UserCheckMiddleware())
    dispatcher.update.middleware(ErrorHandlerMiddleware())


    bot = SafeBot(token=settings.funnel_bot_token, default=DefaultBotProperties(
        protect_content=True,
        parse_mode=ParseMode.MARKDOWN
        )
    )

    await dispatcher.start_polling(bot)