from src.scheduler.tasks import SendMessageTask
from src.scheduler.tasks import SendDocumentTask
from src.scheduler.tasks import SendMessageWithKeyboardTask
from src.safe_bot import SafeBot



class TaskFactory:
    def __init__(self):
        self.registry = {
            "send_message" : SendMessageTask,
            "send_document" : SendDocumentTask,
            "send_message_with_keyboard" : SendMessageWithKeyboardTask,
        }

    def create_task_with_bot(self, task_type, bot: SafeBot, payload: dict):
        handler_class = self.registry.get(task_type)
        if not handler_class:
            raise ValueError(f"Unknown task type: {task_type}")
        return handler_class(bot, payload)

