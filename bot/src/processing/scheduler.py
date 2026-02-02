from src.core.config import config
from src.processing.streams_objects.user_task_stream_message import UserTaskStreamMessage
from src.views.tasks import get_no_processed

import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, redis, stream_key):
        self.redis = redis
        self.stream_key = stream_key
        self.pushed_tasks_key = "scheduler:pushed_tasks"
        self.pushed_tasks_ttl = 3600

    async def push_ready_tasks(self):
        try:
            now = datetime.now(config['TIMEZONE'])

            ready_tasks = await get_no_processed(now)

            if not ready_tasks:
                logger.info("Not ready tasks found")
                return

            logger.info(f"Found {len(ready_tasks)} ready tasks")

            for task in ready_tasks:
                task_key = f"task:{task.id}"
                already_pushed = await self.redis.sismember(self.pushed_tasks_key, task_key)

                if already_pushed:
                    logger.info(f"Task {task.id} already pushed, skipping")
                    continue

                if task.user.is_message_blocked:
                    task.processed = True
                    await task.save()
                    continue

                stream_msg_task = UserTaskStreamMessage(
                    task_id=task.id,
                    task_type=task.type,
                    payload=task.payload,
                    user_id=task.user_id
                )

                await self.redis.xadd(self.stream_key, stream_msg_task.to_dict())
                await self.redis.sadd("scheduler:pushed_tasks", f"task:{task.id}")
                logger.info(f"Task {task.id} pushed to stream")

        except Exception as e:
            logger.error(f"Error in push_ready_tasks: {e}", exc_info=True)