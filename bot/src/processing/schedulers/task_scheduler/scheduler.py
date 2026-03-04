import asyncio

from src.core.logging_config import setup_logging

logger = setup_logging(__name__, service="task_scheduler")

from redis.exceptions import LockError

from src.views.user_state.get_inactive_users import get_inactive_users

from arq import create_pool
from arq.connections import RedisSettings
from redis.asyncio.lock import Lock
from tortoise.transactions import in_transaction

from src.core.config import settings
from src.views.sent_message.get_expires_messages import get_expires_messages
from src.views.tasks import get_no_processed_tasks
from src.core.redis import init_redis

from datetime import datetime, timezone


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

    async def _get_inactive_users(self):
        users = await get_inactive_users(datetime.now(timezone.utc))

        for user in users:
            job = await self.arq_pool.enqueue_job(
                'send_nudge',
                telegram_user_id=user.telegram_id,
                _job_id=f"send_nudge_{user.telegram_id}",
                _queue_name='messages_for_users'
            )

            if job:
                logger.info(f"Message {user.telegram_id} enqueued for deletion")
            else:
                logger.warning(f"Message {user.telegram_id} duplicate")

    async def push_tasks(self):
        """
        Основной цикл scheduler'а

        1. Берёт lock в Redis (только один scheduler может работать)
        2. Обрабатывает готовые таски
        3. Находит истекшие сообщения для удаления
        4. Отправляет напоминания неактивным юзерам
        """
        redis_client = None
        arq_pool = None

        try:
            # Инициализируем Redis
            redis_client = init_redis()

            # Пытаемся получить lock
            async with Lock(
                    redis_client,
                    name=settings.scheduler_lock_key,
                    timeout=70,
                    blocking_timeout=1,
            ) as lock:

                # Проверяем что lock принадлежит нам
                if not await lock.owned():
                    logger.info("⏭️ Another scheduler is running, skipping...")
                    return

                logger.info("🔒 Lock acquired, processing tasks...")

                # Создаём ARQ pool
                arq_pool = await create_pool(RedisSettings(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    database=settings.redis_db,
                ))

                self.arq_pool = arq_pool

                # Параллельно выполняем все задачи
                results = await asyncio.gather(
                    self._get_ready_tasks(),
                    self._get_expired_message(),
                    self._get_inactive_users(),
                    return_exceptions=True
                )

                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        task_names = ["ready_tasks", "expired_messages", "inactive_users"]
                        logger.error(f"❌ Error in {task_names[i]}: {result}", exc_info=result)

        except LockError as e:
            logger.warning(f"⚠️ Failed to acquire lock: {e}")

        except Exception as e:
            logger.error(f"💥 Critical error in push_tasks: {e}", exc_info=True)

        finally:
            if arq_pool:
                try:
                    await arq_pool.close()
                    logger.debug("ARQ pool closed")
                except Exception as e:
                    logger.error(f"Error closing ARQ pool: {e}")

            if redis_client:
                try:
                    await redis_client.close()
                    logger.debug("Redis client closed")
                except Exception as e:
                    logger.error(f"Error closing Redis client: {e}")


