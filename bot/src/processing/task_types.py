from enum import Enum


class TaskTypeEnum(str, Enum):
    """Типы тасок для фабрики"""

    # Messaging
    SEND_MESSAGE = "send_message"
    SEND_DOCUMENT = "send_document"
    SEND_VIDEO = "send_video"
    SEND_VIDEO_NOTE = "send_video_note"

    # Discount operations
    SET_DISCOUNT_AND_SEND_MESSAGE = "set_discount_and_send_message_task"
    REMOVE_DISCOUNT_AND_SEND_MESSAGE = "remove_discount_and_send_message_task"

    # Funnel operation
    FINISH_FUNNEL = "finish_funnel"