from src.models.scheduled_task import ScheduledTask
from datetime import datetime


async def create_task(user_id, task_type, payload, run_at: datetime, connection=None):
    if connection:
        await ScheduledTask.create(
            user_id=user_id,
            type=task_type,
            payload=payload,
            run_at=run_at,
            using_db=connection,
        )
    else:
        await ScheduledTask.create(
            user_id=user_id,
            type=task_type,
            payload=payload,
            run_at=run_at,
        )