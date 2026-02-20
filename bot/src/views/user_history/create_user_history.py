from src.models import UserHistory


async def create_user_history(user_id, event_type, user_stage, payload = None, connection = None):
    if connection:
        await UserHistory.create(
            user_id=user_id,
            event_type=event_type,
            stage=user_stage,
            payload=payload,
            using_db=connection,
        )
    else:
        await UserHistory.create(
            user_id=user_id,
            event_type=event_type,
            stage=user_stage,
            payload=payload,
        )
