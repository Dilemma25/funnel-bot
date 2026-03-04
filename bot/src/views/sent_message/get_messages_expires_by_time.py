from src.models import SentMessage
from src.core.config import settings

from datetime import datetime


async def get_expires_messages_by_time():
    messages = await SentMessage.filter(
        delete_at__lte=datetime.now(settings.timezone),
        is_deleted=False,
    )

    return messages