from src.core.config import config
from src.core.database import init_db
from src.middlewares.user_check import UserCheckMiddleware
from src.safe_bot import SafeBot
from src.core import init_redis

from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.enums import ParseMode
from tortoise import run_async
from .setap_routers import setup_routers

async def start_app() -> None:
    run_async(init_db())

    redis = init_redis()
    storage = RedisStorage(redis)

    dispatcher = Dispatcher(storage=storage)

    dispatcher.include_router(setup_routers())

    dispatcher.message.middleware(UserCheckMiddleware())

    bot = SafeBot(token=config["BOT_TOKEN"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dispatcher.start_polling(bot)