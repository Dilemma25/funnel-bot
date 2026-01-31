from src.scheduler.task_types import SendMessageTask
from src.safe_bot import SafeBot


class TaskFactory:
    def __init__(self):
        self.registry = {
            "send_message" : SendMessageTask
        }

    def create_task_with_bot(self, task_type, bot: SafeBot, payload: dict):
        handler_class = self.registry.get(task_type)
        if not handler_class:
            raise ValueError(f"Unknown task type: {task_type}")
        return handler_class(bot, payload)

