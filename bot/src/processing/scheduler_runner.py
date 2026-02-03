import asyncio
import logging

from src.core.database import init_db, close_db
from src.processing.scheduler import Scheduler


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Scheduler: запуск")
    is_db_init = False

    try:
        await init_db()
        is_db_init = True

        scheduler = Scheduler()

        await scheduler.push_ready_tasks()

    except Exception as e:
        logger.error(f"Ошибка в Scheduler: {e}", exc_info=True)

    finally:
        logger.info("Scheduler: завершил обработку задач")
        if is_db_init:
            await close_db()


if __name__ == "__main__":
    asyncio.run(main())