from .get_messages_expires_by_time import get_expires_messages_by_time
from .get_messages_expires_by_delete_on_stage import get_messages_to_delete_by_stage

from typing import List
from src.models import SentMessage

async def get_expires_messages() -> List[SentMessage]:
    expires_by_time = await get_expires_messages_by_time()
    expires_by_stage = await get_messages_to_delete_by_stage()

    all_messages = {msg.id: msg for msg in (expires_by_time + expires_by_stage)}
    result = list(all_messages.values())

    return result