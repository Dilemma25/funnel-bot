from src.models import ScheduledTask
#
# async def get_no_processed(conn, time):
#     return await (ScheduledTask.filter(
#         processed = False,
#         run_at__lte = time,
#     ).using_db(conn).
#       order_by("run_at").
#       prefetch_related("user").
#       select_for_update())


async def get_no_processed(time):
    return await (ScheduledTask.filter(
        processed = False,
        run_at__lte = time,
    ).
      order_by("run_at").
      prefetch_related("user").
      select_for_update())