import asyncio

from src.core.database import close_db
from src.core.database import init_db
from src.core.logging_config import setup_logging
from src.processing.schedulers.task_scheduler.scheduler import Scheduler

logger = setup_logging(__name__, service="task_scheduler")


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