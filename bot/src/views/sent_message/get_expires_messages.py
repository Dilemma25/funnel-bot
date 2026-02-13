from datetime import datetime

from src.core.config import settings
from src.models import SentMessage


async def get_expires_messages():
    messages = await SentMessage.filter(
        delete_at__lte=datetime.now(settings.timezone),
        is_deleted=False,
    )

    return messages