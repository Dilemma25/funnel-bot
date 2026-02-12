from src.models import User


async def deactivate_user(user_id: int, connection=None):
    query = User.filter(telegram_id=user_id)

    if connection:
        query = query.using_db(connection)

    user = await query.first()

    if not user:
        return None

    user.is_message_blocked = True

    if connection:
        await user.save(using_db=connection)
    else:
        await user.save()

    return user