from aiogram import BaseMiddleware
from aiogram.types import Update
from aiogram.fsm.context import FSMContext

from src.core.logging_config import setup_logging


logger = setup_logging(__name__, service="bot")


class StateRestoreMiddleware(BaseMiddleware):
    """
    Middleware для восстановления состояния из БД
    если Redis не доступен
    """

    async def __call__(self, handler, event: Update, data):
        state: FSMContext = data.get("state")

        if state:
            try:
                current_state = await state.get_state()

                if current_state:
                    logger.debug(f"✅ State loaded: {current_state}")

            except Exception as e:
                logger.error(f"❌ State restore failed: {e}")

        return await handler(event, data)