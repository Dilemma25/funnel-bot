from src.models import UserLog


async def create_user_log(user_id, event_type, user_stage, payload = None, connection = None):
    if connection:
        await UserLog.create(
            user_id=user_id,
            event_type=event_type,
            stage=user_stage,
            payload=payload,
            using_db=connection,
        )
    else:
        await UserLog.create(
            user_id=user_id,
            event_type=event_type,
            stage=user_stage,
            payload=payload,
        )
