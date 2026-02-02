from src.models import User

async def deactivate_user(user_id: int):
    user = await User.get(telegram_id=user_id)
    user.is_message_blocked = True
    await user.save()