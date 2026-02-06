from .send_document import SendDocumentTask
from .send_message import SendMessageTask
from .send_message_with_keyboard import SendMessageWithKeyboardTask
from .send_video_note import SendVideoNoteTask
from .send_video import SendVideoTask
from .remove_discount_and_send_message import RemoveDiscountAndSendMessageTask

__all__ = [
    'SendMessageTask',
    'SendDocumentTask',
    'SendMessageWithKeyboardTask',
    'SendVideoNoteTask',
    'SendVideoTask',
    'RemoveDiscountAndSendMessageTask'
]



