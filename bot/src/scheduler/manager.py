from datetime import datetime
from datetime import timezone

import logging

from src.scheduler.task_factory import TaskFactory
from src.views.tasks import get_no_processed



class TaskManager:

    def __init__(self, bot, connection):
        self.bot = bot
        self.connection = connection
        self.task_factory = TaskFactory()

    async def run_once(self):
        now = datetime.now(timezone.utc)

        tasks = await get_no_processed(self.connection, now)

        for task in tasks:
            try:
                if task.user.is_message_blocked:
                    task.processed = True
                    await task.save(using_db=self.connection)
                    continue

                handler = self.task_factory.create_task_with_bot(task.type, self.bot, task.payload)
                await handler.execute()
                task.processed = True
                await task.save(using_db=self.connection)
            except Exception as e:
                logging.error(f"Ошибка при выполнении задачи {task.id}: {e}", exc_info=True)