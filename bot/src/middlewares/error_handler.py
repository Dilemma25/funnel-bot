from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Update
from tortoise.transactions import in_transaction

from src.core.logging_config import setup_logging
from src.models.user_offer import UserOfferStatusEnum
from src.views.tasks.cancel_user_tasks import cancel_user_tasks
from src.views.user import deactivate_user
from src.views.user_offer.change_status import change_user_offer_status

logger = setup_logging(__name__, service="bot")


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data):
        try:
            return await handler(event, data)


        except TelegramForbiddenError as e:

            chat_id = None
            if event.message:
                chat_id = event.message.chat.id
            elif event.callback_query:
                chat_id = event.callback_query.message.chat.id
            elif event.inline_query:
                chat_id = event.inline_query.from_user.id

            # Можно добавить другие типы апдейтов при необходимости

            if chat_id:
                async with in_transaction() as conn:
                    await deactivate_user(chat_id, conn)
                    await change_user_offer_status(chat_id, UserOfferStatusEnum.BLOCKED_BOT, conn)
                    await cancel_user_tasks(chat_id, conn)

            # Логируем или кидаем дальше

            logger.warning(f"User {chat_id} blocked the bot: {e}")

        except Exception as e:
            logger.error(f"Необработанная ошибка: {e}", exc_info=True)

            # Пытаемся уведомить пользователя
            try:
                if event.message:
                    await event.message.answer(
                        "❌ Произошла ошибка. Мы уже работаем над её исправлением."
                    )
                elif event.callback_query:
                    await event.callback_query.message.answer(
                        "❌ Произошла ошибка. Попробуй позже."
                    )
            except:
                pass  # Если даже это упало, ничего не делаем