from functools import wraps
from aiogram.exceptions import TelegramForbiddenError
from src.views.user.deactivate_user import deactivate_user


def safe_send(func):
    @wraps(func)
    async def wrapper(self, chat_id: int, *args, **kwargs):
        try:
            return await func(self, chat_id, *args, **kwargs)
        except TelegramForbiddenError:
            await deactivate_user(chat_id)
        except Exception as e:
            print(f"Error: {e}")
    return wrapper
