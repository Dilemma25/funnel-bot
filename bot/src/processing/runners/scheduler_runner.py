import asyncio
import logging

from src.core import init_redis
from src.core.database import init_db, close_db
from src.processing.locks import RedisLock
from src.core.config import config
from src.processing.scheduler import Scheduler


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
        if not await redis_lock.acquire():
            logger.info("Scheduler уже работает, пропускаю")
            return


        await init_db()
        is_db_init = True

        redis = init_redis()
        scheduler = Scheduler(redis, config["REDIS_STREAM_KEY"])

        await scheduler.push_ready_tasks()


    except Exception as e:
        logger.error(f"Ошибка в Scheduler: {e}", exc_info=True)

    finally:
        logger.info("Scheduler: завершил обработку задач")
        await redis_lock.release()
        await redis_lock.close()
        if is_db_init:
            await close_db()


if __name__ == "__main__":
    asyncio.run(main())