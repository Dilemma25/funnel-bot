from src.models import User


async def get_or_create_user(telegram_id: int):
    user, created = await User.get_or_create(
        telegram_id=telegram_id,
    )
    return user, created
