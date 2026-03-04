from src.models import SentMessage
from src.models import UserState
from src.core.config import settings
from src.controllers.user_states import get_stage_order

from typing import List
from datetime import datetime

async def get_messages_to_delete_by_stage(
        connection=None
) -> List[SentMessage]:
    # 1. Получаем все user_states
    user_states_query = UserState.filter(
        user__is_message_blocked=False
    )

    if connection:
        user_states_query = user_states_query.using_db(connection)

    user_states = await user_states_query.all()

    if not user_states:
        return []

    # 2. Создаём mapping {user_id: {current_stage, current_order}}
    user_stage_info = {}
    for us in user_states:
        order = get_stage_order(us.state)
        if order > 0:
            user_stage_info[us.user_id] = {
                'stage': us.state,
                'order': order
            }

    if not user_stage_info:
        return []

    # 3. Получаем сообщения только для юзеров с валидным stage, которые по времени еще не истекли
    messages_query = SentMessage.filter(
        user_id__in=list(user_stage_info.keys()),
        delete_at__gt=datetime.now(settings.timezone),
        is_deleted=False,
    )

    if connection:
        messages_query = messages_query.using_db(connection)

    all_messages = await messages_query.all()

    # 4. Фильтруем
    messages_to_delete = []

    for message in all_messages:
        user_info = user_stage_info.get(message.user_id)

        if not user_info:
            continue

        message_order = get_stage_order(message.delete_on_stage)

        if message_order == 0:
            continue

        # Если current_order >= message_order → удаляем
        if user_info['order'] >= message_order:
            messages_to_delete.append(message)

    return messages_to_delete