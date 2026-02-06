from src.models import ScheduledTask

async def get_no_processed_tasks(time, connection):
    return await (ScheduledTask.filter(
        processed = False,
        run_at__lte = time,
        user__is_message_blocked=False,
    ).using_db(connection).
      order_by("run_at").
      select_for_update()
                  )

# #TODO подумать над тем, чтоб обернуть в транзакцию и завести разные статусы тасок, например(in_progress, complited)
# async def get_no_processed(time):
#     return await (ScheduledTask.filter(
#         processed = False,
#         run_at__lte = time,
#         user__is_message_blocked = False,
#     ).
#       order_by("run_at")
#     )