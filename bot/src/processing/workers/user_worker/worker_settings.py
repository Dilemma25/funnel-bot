import asyncio

from arq.connections import RedisSettings
from tortoise.transactions import in_transaction

from src.core.config import config

import logging

from src.models import ScheduledTask
from src.safe_bot import SafeBot
from src.core.database import init_db
from src.core.redis import init_redis
from src.processing.task_factory import TaskFactory

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def startup(ctx):

    logger.info("<< Worker starting up ... >>")

    await init_db()

    ctx["bot"] = SafeBot(config["BOT_TOKEN"])
    ctx["task_factory"] = TaskFactory()
    ctx["redis"] = init_redis()

    logger.info("<< Worker initialized! >>")

async def shutdown(ctx):
    from src.core.database import close_db

    logger.info("Worker shutting down...")
    await ctx["bot"].session.close()

    if "redis" in ctx:
        ctx["redis"].close()

    await close_db()

    logger.info("<< Worker shutdown >>")

async def send_scheduled_message(ctx, task_id, task_type, payload):
    """
        Основная функция обработки задачи - заменяет handle_message из consumer

        Args:
            ctx: Контекст от arq (содержит bot, task_factory, redis)
            task_id: ID задачи из БД
            task_type: Тип задачи (send_message, send_document и т.д.)
            payload: Данные для задачи
    """

    logger.info(f"Processing task {task_id}: {task_type}")

    try:

        bot: SafeBot = ctx["bot"]
        task_factory: TaskFactory = ctx["task_factory"]

        handler = task_factory.create_task_with_bot(
            task_type=task_type,
            bot=bot,
            payload=payload
        )

        async with in_transaction() as conn:
            task = await ScheduledTask.get(id=task_id, using_db=conn)

            if not task.processed and hasattr(handler, "prepare"):

                await handler.prepare(conn)

                task = await ScheduledTask.get(id=task_id, using_db=conn.connection)
                task.processed = True
                await task.save()

        await handler.execute()

        logger.info(f"Task {task_id} completed and saved to DB")

        await asyncio.sleep(1)

    except Exception as e:
        logger.error(f"Error handling task {task_id}: {e}", exc_info=True)


class WorkerSettings:
    """Настройки arq worker"""

    redis_settings = RedisSettings(
        host=config['REDIS']['HOST'],
        port=int(config['REDIS']['PORT']),
        database=int(config['REDIS']['DB']),
    )

    functions = [send_scheduled_message]

    max_jobs = 1

    job_timeout = 60

    keep_result = 3600

    max_tries = 3

    on_startup = startup
    on_shutdown = shutdown

    health_check_interval = 60

    queue_name = "messages_for_users"


