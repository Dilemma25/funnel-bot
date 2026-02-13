from src.models import ScheduledTask


async def get_no_processed_tasks(time, connection=None):
    query = (
        ScheduledTask.filter(
            processed=False,
            run_at__lte=time,
            user__is_message_blocked=False,
        )
        .order_by("run_at")
        .select_for_update()
    )

    if connection:
        query = query.using_db(connection)

    return await query