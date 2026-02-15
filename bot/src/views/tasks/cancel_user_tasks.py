from src.models import ScheduledTask

#TODO это надо будет переделать, если будут новые  оферы
async def cancel_user_tasks(user_id: int, connection = None):
    """
    Отменить все невыполненные задачи юзера

    Вызывается когда:
    - Юзер купил
    - Юзер заблокировал бота
    - Воронка завершена
    """
    if connection:
        await ScheduledTask.filter(
            user_id=user_id,
            processed=False
        ).using_db(connection).update(
            processed=True
        )
    else:
        await ScheduledTask.filter(
            user_id=user_id,
            processed=False
        ).update(
            processed=True
        )