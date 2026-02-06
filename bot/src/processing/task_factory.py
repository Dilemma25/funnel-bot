from src.processing.tasks.messaging import SendMessageTask
from src.processing.tasks.messaging import SendDocumentTask
from src.processing.tasks.messaging import SendMessageWithKeyboardTask
from src.processing.tasks.messaging import SendVideoNoteTask
from src.processing.tasks.messaging import SendVideoTask
from src.processing.tasks.messaging import RemoveDiscountAndSendMessageTask
from src.safe_bot import SafeBot


class TaskFactory:
    def __init__(self):
        self.registry = {
            "send_message" : SendMessageTask,
            "send_document" : SendDocumentTask,
            "send_message_with_keyboard" : SendMessageWithKeyboardTask,
            "send_video_note" : SendVideoNoteTask,
            "send_video" : SendVideoTask,
            "remove_discount_and_send_message_task" : RemoveDiscountAndSendMessageTask
        }

    def create_task_with_bot(self, task_type, bot: SafeBot, payload: dict):
        handler_class = self.registry.get(task_type)
        if not handler_class:
            raise ValueError(f"Unknown task type: {task_type}")
        return handler_class(bot, payload)