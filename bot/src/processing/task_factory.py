from src.processing.tasks.messaging import SendMessageTask
from src.processing.tasks.messaging import SendDocumentTask
from src.processing.tasks.messaging import SendVideoNoteTask
from src.processing.tasks.messaging import SendVideoTask
from src.processing.tasks.messaging import RemoveDiscountAndSendMessageTask
from src.processing.tasks.messaging.set_discount_and_send_message import SetDiscountAndSendMessageTask
from src.safe_bot import SafeBot
from src.processing.task_types import TaskTypeEnum


class TaskFactory:
    def __init__(self):
        self.registry = {
            TaskTypeEnum.SEND_MESSAGE : SendMessageTask,
            TaskTypeEnum.SEND_DOCUMENT : SendDocumentTask,
            TaskTypeEnum.SEND_VIDEO_NOTE : SendVideoNoteTask,
            TaskTypeEnum.SEND_VIDEO : SendVideoTask,

            TaskTypeEnum.REMOVE_DISCOUNT_AND_SEND_MESSAGE : RemoveDiscountAndSendMessageTask,
            TaskTypeEnum.SET_DISCOUNT_AND_SEND_MESSAGE : SetDiscountAndSendMessageTask,
        }

    def create_task_with_bot(self, task_type, bot: SafeBot, payload: dict):
        handler_class = self.registry.get(task_type)
        if not handler_class:
            raise ValueError(f"Unknown task type: {task_type}")
        return handler_class(bot, payload)