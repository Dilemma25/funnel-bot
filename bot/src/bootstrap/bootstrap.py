from src.core.config import config
from src.core.database import init_db
from src.middlewares.user_check import UserCheckMiddleware
from src.safe_bot import SafeBot
from src.core import init_redis

from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from tortoise import run_async
from .setap_routers import setup_routers
from ..core.hybrid_storage import HybridStorage
from ..middlewares.error_handler import ErrorHandlerMiddleware
from src.middlewares.state_restore import StateRestoreMiddleware
from aiogram.fsm.storage.redis import RedisStorage

async def start_app() -> None:
    run_async(init_db())

    redis = init_redis()
    redis_storage = RedisStorage(redis)
    storage = HybridStorage(redis_storage)

    dispatcher = Dispatcher(storage=storage)

    dispatcher.include_router(setup_routers())

    dispatcher.message.middleware(UserCheckMiddleware())
    dispatcher.update.middleware(ErrorHandlerMiddleware())
    dispatcher.update.middleware(StateRestoreMiddleware())


    bot = SafeBot(token=config["BOT_TOKEN"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dispatcher.start_polling(bot)