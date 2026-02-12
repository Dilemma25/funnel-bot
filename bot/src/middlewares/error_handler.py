from aiogram import BaseMiddleware
from aiogram.types import Update

from src.core.logging_config import setup_logging


logger = setup_logging(__name__, service="bot")


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data):
        try:
            return await handler(event, data)

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