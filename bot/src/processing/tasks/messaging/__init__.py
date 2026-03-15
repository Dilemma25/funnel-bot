from .send_document import SendDocumentTask
from .send_message import SendMessageTask
from .send_video_note import SendVideoNoteTask
from .send_video import SendVideoTask
from .remove_discount_and_send_message import RemoveDiscountAndSendMessageTask
from .finish_funnel import FinishFunnelTask

__all__ = [
    'SendMessageTask',
    'SendDocumentTask',
    'SendVideoNoteTask',
    'SendVideoTask',
    'RemoveDiscountAndSendMessageTask',
    'FinishFunnelTask'
]



