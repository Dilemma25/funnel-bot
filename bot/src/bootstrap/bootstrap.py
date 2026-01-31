from src.core.config import config
from src.core.database import init_db
from src.safe_bot import SafeBot
from src.dispatcher import dispatcher

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from tortoise import run_async


async def start_app() -> None:
    run_async(init_db())

    bot = SafeBot(token=config["BOT_TOKEN"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dispatcher.start_polling(bot)