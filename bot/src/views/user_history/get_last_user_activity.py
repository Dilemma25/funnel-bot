from src.models import UserHistory
from src.models.user_history import EventTypeEnum


async def get_last_user_activity(
        user_id: int,
        connection = None
) -> UserHistory | None:
    query = UserHistory.filter(
        user_id=user_id,
        event_type__in=[EventTypeEnum.BUTTON_CLICKED, EventTypeEnum.STAGE_ENTERED]
    )
    if connection:
        result = await query.using_db(connection).order_by("-created_at").first()
    else:
        result = await query.order_by("-created_at").first()
    return result