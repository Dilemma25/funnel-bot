from src.models.scheduled_task import ScheduledTask
from datetime import datetime

async def create(user_id, task_type, payload, run_at: datetime):
    await ScheduledTask.create(
        user_id=user_id,
        type=task_type,
        payload=payload,
        run_at=run_at,
    )