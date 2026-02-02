import asyncio
import logging
from src.core.database import init_db
from src.core.database import close_db
from src.safe_bot import SafeBot
from src.scheduler.locks import acquire_lock
from src.scheduler.locks import release_lock
from src.core.config import config
from src.scheduler.manager import TaskManager

from tortoise import Tortoise

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#TODO доделать чтоб не было 2 крона в один момент времени, скорее всего через grep
async def main():


    logger.info("Scheduler: запуск")
    await init_db()
    logger.info("DB инициализирована")

    connection = Tortoise.get_connection("default")

    lock_acquired = await acquire_lock(connection)
    logger.info(f"Lock acquired: {lock_acquired}")

    if not lock_acquired:
        logger.info("Scheduler: уже работает, пропускаю")
        await close_db()
        return

    try:
        bot = SafeBot(token=config["BOT_TOKEN"])
        manager = TaskManager(bot, connection)

        logger.info("Начинаю обработку задач")
        await manager.run_once()
        logger.info("Scheduler: завершил обработку задач")

    except Exception as e:
        logger.error(f"Ошибка в scheduler: {e}", exc_info=True)


    finally:
        logger.info("Releasing lock...")
        released = await release_lock(connection)
        logger.info(f"Lock released: {released}")  # ← должно быть True
        await close_db()


if __name__ == "__main__":
    asyncio.run(main())