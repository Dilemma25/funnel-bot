from src.core.logging_config import setup_logging
logger = setup_logging(__name__, service="task_scheduler")

from arq import create_pool
from arq.connections import RedisSettings
from redis.asyncio.lock import Lock
from tortoise.transactions import in_transaction

from src.core.config import settings
from src.views.sent_message.get_expires_messages import get_expires_messages
from src.views.tasks import get_no_processed_tasks
from src.core.redis import init_redis

from datetime import datetime




class Scheduler:
    def __init__(self):
        self.arq_pool = None

    async def _get_ready_tasks(self):

        now = datetime.now(settings.timezone)

        async with in_transaction() as conn:
            ready_tasks = await get_no_processed_tasks(now, conn)

        if not ready_tasks:
            logger.info("No ready tasks found")
            return

        logger.info(f"Found {len(ready_tasks)} ready tasks")

        for task in ready_tasks:

            job = await self.arq_pool.enqueue_job(
                'send_scheduled_message',
                task_id=task.id,
                task_type=task.type,
                payload=task.payload,
                _job_id=f"task_{task.id}",
                _queue_name='messages_for_users'
            )

            if job:
                logger.info(f"Task {task.id} enqueued to arq with job_id={job.job_id}")
            else:
                logger.warning(f"Task {task.id} already in arq queue (duplicate)")

        logger.info(f"Successfully enqueued {len(ready_tasks)} tasks")

    async def _get_expired_message(self):
        messages = await get_expires_messages()

        for message in messages:
            job = await self.arq_pool.enqueue_job(
                'delete_message',  # ← Функция 2
                message_id=message.id,
                telegram_message_id=message.telegram_message_id,
                chat_id=message.user_id,
                message_tag=message.tag,
                _job_id=f"delete_msg_{message.id}",
                _queue_name='messages_for_users'
            )

            if job:
                logger.info(f"Message {message.id} enqueued for deletion")
            else:
                logger.warning(f"Message {message.id} duplicate")

        logger.info(f"Successfully enqueued {len(messages)} messages on delete")


    async def push_tasks(self):
        redis_client = init_redis()

        try:
            async with Lock(
                    redis_client,
                    name=settings.scheduler_lock_key,
                    timeout=70,
                    blocking_timeout=1,
            ) as lock:

                if not await lock.owned():
                    logger.info("Another scheduler is running, skipping...")
                    return

                logger.info("Lock acquired, processing tasks...")

                self.arq_pool = await create_pool(RedisSettings(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    database=settings.redis_db,
                    )
                )

                await self._get_ready_tasks()
                await self._get_expired_message()

        except Exception as e:
            logger.error(f"Error in push_ready_tasks: {e}", exc_info=True)

        finally:
            if self.arq_pool:
                await self.arq_pool.close()
                logger.info("ARQ pool closed")

            await redis_client.close()


