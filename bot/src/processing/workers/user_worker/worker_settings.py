import asyncio

from aiogram.exceptions import TelegramBadRequest
from arq.connections import RedisSettings
from arq import Retry
from tortoise.transactions import in_transaction

from src.core.config import settings
from src.core.logging_config import setup_logging
from src.models import ScheduledTask
from src.processing.tasks.preparable import PreparableTask
from src.safe_bot import SafeBot
from src.core.database import init_db
from src.core.redis import init_redis
from src.processing.task_factory import TaskFactory
from src.views.sent_message import mark_message_as_deleted

logger = setup_logging(__name__, service="user_worker")


async def startup(ctx):

    logger.info("<< Worker starting up ... >>")

    await init_db()

    ctx["bot"] = SafeBot(settings.bot_token)
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

    bot: SafeBot = ctx["bot"]
    task_factory: TaskFactory = ctx["task_factory"]

    job_try = ctx.get("job_try", 1)
    max_tries = ctx.get("max_tries", 3)

    try:

        handler = task_factory.create_task_with_bot(
            task_type=task_type,
            bot=bot,
            payload=payload
        )

        async with in_transaction() as conn:

            task = await ScheduledTask.filter(id=task_id).using_db(conn).first()

            #Если таска не выполнялась
            if not task.processed:
                #Если таска работает с бд
                if isinstance(handler, PreparableTask):

                    await handler.prepare(conn)

                    await task.refresh_from_db(using_db=conn)
                    await task.save(using_db=conn)

                task.processed = True
                await task.save(using_db=conn)

        await handler.execute()

        logger.info(f"Task {task_id} completed and saved to DB")

        await asyncio.sleep(1)

    except Exception as e:
        logger.error(f"Error handling task {task_id}: {e}", exc_info=True)

        if job_try < max_tries:
            # Delays will be 5s, 10s, 15s
            defer_by = job_try * 5
            print(f"Retrying in {defer_by} seconds...")
            raise Retry(defer=defer_by) from e

        raise Exception("Connection Error: The service is currently unavailable. Please try again later.")

#TODO протестировать
async def delete_message(
                         ctx,
                         message_id,
                         telegram_message_id,
                         chat_id,
                         message_tag,
                     ):
    """Удаление истекших сообщений"""

    logger.info(f"Deleting message {message_id} (tg_msg={telegram_message_id})")

    bot = None

    if message_tag != 'course':
        bot = ctx["bot"]

    try:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=telegram_message_id)
            logger.info(f"✅ Message {telegram_message_id} deleted from Telegram")

        except TelegramBadRequest as e:
            if "message to delete not found" in str(e).lower():
                logger.warning(f"⚠️ Message {telegram_message_id} already deleted")
            else:
                raise

        async with in_transaction() as conn:
            await mark_message_as_deleted(message_id, conn)

        logger.info(f"✅ Message {message_id} marked as deleted")

    except Exception as e:
        logger.error(f"❌ Error deleting message {message_id}: {e}", exc_info=True)


class WorkerSettings:
    """Настройки arq worker"""

    redis_settings = RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
        database=settings.redis_db
    ),


    functions = [send_scheduled_message]

    max_jobs = 1

    job_timeout = 60

    keep_result = 3600

    max_tries = 3

    on_startup = startup
    on_shutdown = shutdown

    health_check_interval = 60

    queue_name = "messages_for_users"


