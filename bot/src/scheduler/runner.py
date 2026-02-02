import asyncio
import logging
from src.core.database import init_db
from src.core.database import close_db
from src.safe_bot import SafeBot
from src.scheduler.locks import RedisLock
from src.core.config import config
from src.scheduler.manager import TaskManager

from tortoise import Tortoise

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    redis_lock = RedisLock()
    redis_lock.connect()

    logger.info("Scheduler: запуск")
    is_db_init = False

    try:
        print(f"DEBUG: Trying to acquire lock...")
        if not await redis_lock.acquire():
            logger.info("Scheduler уже работает, пропускаю")
            return

        print(f"DEBUG: Lock acquired!")

        await init_db()
        is_db_init = True
        logger.info("DB инициализирована")

        connection = Tortoise.get_connection("default")

        bot = SafeBot(token=config["BOT_TOKEN"])
        manager = TaskManager(bot, connection)

        logger.info("Начинаю обработку задач")
        await manager.run_once()
        logger.info("Scheduler: завершил обработку задач")

    except Exception as e:
        logger.error(f"Ошибка в scheduler: {e}", exc_info=True)

    finally:
        logger.info("Releasing lock...")
        print(f"DEBUG: Releasing lock...")
        await redis_lock.release()
        logger.info("Lock released")
        await redis_lock.close()
        if is_db_init:
            await close_db()


if __name__ == "__main__":
    asyncio.run(main())