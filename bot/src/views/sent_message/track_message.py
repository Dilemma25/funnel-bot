from src.models import SentMessage
from datetime import datetime


async def track_message(
        user_id: int,
        telegram_message_id: int,
        tag: str = None,
        stage: str = None,
        delete_on_stage: str = None,
        delete_at: datetime = None,
        connection=None
):
    """
    Сохранить сообщение для отслеживания

    Args:
        user_id: ID пользователя
        telegram_message_id: ID сообщения в Telegram
        tag: Тег для группировки
        stage: Текущий этап
        delete_at: Удалить в N
        delete_on_stage: Удалить при переходе на стадию
        connection: DB connection
    """
    if connection:
        await SentMessage.create(
            user_id=user_id,
            telegram_message_id=telegram_message_id,
            tag=tag,
            stage=stage,
            delete_at=delete_at,
            delete_on_stage=delete_on_stage,
        )
    else:
        await SentMessage.create(
            user_id=user_id,
            telegram_message_id=telegram_message_id,
            tag=tag,
            stage=stage,
            delete_at=delete_at,
            delete_on_stage=delete_on_stage,
            using_db=connection,
        )