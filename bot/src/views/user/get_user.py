from src.models import User


async def get_user(user_id: int, connection=None):

    query = User.filter(telegram_id=user_id)

    if connection:
        user = await query.using_db(connection).first()
    else:
        user = await query.first()

    return user