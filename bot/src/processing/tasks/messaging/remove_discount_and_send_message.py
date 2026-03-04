from src.views.user_state.update_user_state import update_user_state
from .base_messaging import BaseMessagingTask
from src.processing.tasks.preparable import PreparableTask
from src.views.user_offer import remove_discount

from aiogram.types import Message


class RemoveDiscountAndSendMessageTask(BaseMessagingTask, PreparableTask):

    async def prepare(self, connection):

        await remove_discount(
            user_id=self.payload["user_id"],
            offer_code=self.payload["offer_code"],
            connection=connection
        )

        await self.update_user_state(connection)

        return True

    async def execute(self) -> Message:
        keyboard = self._build_keyboard()

        message = await self.bot.send_message(
            chat_id=self.payload["user_id"],
            text=self.payload["text"],
            reply_markup=keyboard,
            parse_mode="Markdown",
            protect_content=True,
        )

        return message