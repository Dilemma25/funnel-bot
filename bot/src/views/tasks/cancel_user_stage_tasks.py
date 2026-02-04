from src.models import ScheduledTask


async def cancel_user_stage_tasks(user_id, stage: str):
    tasks = await ScheduledTask.filter(
        user_id=user_id,
        processed=False,
        payload__state=stage,
    )

    for task in tasks:
        task.processed = True
        await task.save()