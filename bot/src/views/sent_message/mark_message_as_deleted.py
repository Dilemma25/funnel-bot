from src.models import SentMessage
from src.core.config import settings

from datetime import datetime

async def mark_message_as_deleted(message_id: int, connection=None):
    """Пометить сообщение как удаленное"""

    query = SentMessage.filter(id=message_id)

    if connection:
        query = query.using_db(connection)

    message = await query.first()

    if message:
        message.is_deleted = True
        message.deleted_at = datetime.now(settings.timezone)

        if connection:
            await message.save(using_db=connection)
        else:
            await message.save()

    return message