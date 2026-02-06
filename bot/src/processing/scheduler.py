from arq import create_pool
from arq.connections import RedisSettings
from redis.asyncio import Redis
from redis.asyncio.lock import Lock
from tortoise.transactions import in_transaction

from src.core.config import config
from src.views.tasks import get_no_processed_tasks

import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self):
        self.arq_pool = None

    async def push_ready_tasks(self):
        redis_client = Redis(
            host=config["REDIS"]["HOST"],
            port=int(config["REDIS"]["PORT"]),
            db=int(config["REDIS"]["DB"]),
            decode_responses=True
        )

        try:
            async with Lock(
                    redis_client,
                    name=config["SCHEDULER_LOCK_KEY"],
                    timeout=70,
                    blocking_timeout=1,
            ) as lock:

                if not await lock.owned():
                    logger.info("Another scheduler is running, skipping...")
                    return

                logger.info("Lock acquired, processing tasks...")

                self.arq_pool = await create_pool(RedisSettings(
                    host=config["REDIS"]["HOST"],
                    port=int(config["REDIS"]["PORT"]),
                    database=int(config["REDIS"]["DB"]),
                ))

                now = datetime.now(config['TIMEZONE'])

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

        except Exception as e:
            logger.error(f"Error in push_ready_tasks: {e}", exc_info=True)

        finally:
            if self.arq_pool:
                await self.arq_pool.close()
                logger.info("ARQ pool closed")

            await redis_client.close()