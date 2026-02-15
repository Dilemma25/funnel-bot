from functools import wraps
from aiogram.exceptions import TelegramForbiddenError
from tortoise.transactions import in_transaction

from src.models.user_offer import UserOfferStatusEnum
from src.views.tasks.cancel_user_tasks import cancel_user_tasks
from src.views.user.deactivate_user import deactivate_user
from src.views.user_offer.change_status import change_user_offer_status


def safe(func):
    @wraps(func)
    async def wrapper(self, chat_id: int, *args, **kwargs):
        try:
            return await func(self, chat_id, *args, **kwargs)
        except TelegramForbiddenError:

            async with in_transaction() as conn:
                await deactivate_user(chat_id, conn)
                await change_user_offer_status(chat_id, UserOfferStatusEnum.BLOCKED_BOT, conn)
                await cancel_user_tasks(chat_id, conn)

        except Exception as e:
            raise e
    return wrapper
