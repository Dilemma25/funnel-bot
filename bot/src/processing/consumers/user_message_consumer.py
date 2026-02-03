import asyncio
import logging
import json

from redis.asyncio import Redis

from src.models import ScheduledTask
from src.processing.task_factory import TaskFactory


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UserMessageConsumer:
    def __init__(
            self,
            bot,
            redis: Redis,
            task_factory: TaskFactory,
            consumer_group,
            consumer_name,
            stream_key,
    ):
        self.bot = bot
        self.redis = redis
        self.task_factory = task_factory
        self.consumer_group = consumer_group
        self.consumer_name = consumer_name
        self.stream_key = stream_key

    async def init_consumer_group(self):
        """Создай consumer group если не существует"""
        try:
            await self.redis.xgroup_create(
                self.stream_key,
                self.consumer_group,
                id="$",
                mkstream=True
            )
            logger.info(f"Consumer group '{self.consumer_group}' created")
        except Exception:
            logger.info(f"Consumer group '{self.consumer_group}' already exists")

    async def process_messages(self):
        await self.init_consumer_group()

        while True:

            # ← Сначала обработай Pending List (задачи которые не были ACKed)
            pending = await self.redis.xautoclaim(
                self.stream_key,
                self.consumer_group,
                self.consumer_name,
                min_idle_time=0,  # Все pending задачи
                start_id="0-0",
                count=10
            )

            if pending[1]:  # pending[1] это сами сообщения
                logger.info(f"Found {len(pending[1])} pending messages")
                for message_id, message_data in pending[1]:
                    await self.handle_message(message_id, message_data)

            messages = await self.redis.xreadgroup(
                streams={self.stream_key:">"},
                groupname=self.consumer_group,
                consumername=self.consumer_name,
                count=10,
                block=1000,
            )

            if not messages:
                continue

            for stream_name, stream_message in messages:
                for message_id, message_data in stream_message:
                    await self.handle_message(message_id, message_data)

    async def handle_message(self, message_id, message_data):
        task_id = None

        try:
            task_id = int(message_data["task_id"])
            task_type = message_data["task_type"]
            payload = json.loads(message_data["payload"])

            logger.info(f"Processing task {task_id}: {task_type}")

            handler = self.task_factory.create_task_with_bot(
                task_type=task_type,
                bot=self.bot,
                payload=payload
            )

            await handler.execute()

            task = await ScheduledTask.get(id=task_id)
            task.processed = True
            await task.save()

            logger.info(f"Task {task_id} completed and saved to DB")
            #TODO подумать над тем чтоб перенести удаление с канала в scheduler
            await asyncio.gather(
                self.redis.xack(self.stream_key, self.consumer_group, message_id),
                self.redis.srem("scheduler:pushed_tasks", f"task:{task_id}"),
                self.redis.xdel(self.stream_key, message_id),
            )

            await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"Error handling task {task_id}: {e}", exc_info=True)