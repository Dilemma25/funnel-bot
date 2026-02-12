from src.models import User


async def get_or_create_user(telegram_id: int, connection=None):
    if connection:
        user = await User.get_or_create(
            telegram_id=telegram_id,
            using_db=connection
        )
    else:
        user = await User.get_or_create(
            telegram_id=telegram_id,
        )
    return user