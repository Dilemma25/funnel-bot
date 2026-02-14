from src.processing.tasks.messaging.base_messaging import BaseMessagingTask
from aiogram.types import Message


class SendMessageTask(BaseMessagingTask):
    async def execute(self) -> Message:

        keyboard = self._build_keyboard()

        message = await self.bot.send_message(
            chat_id=self.payload["user_id"],
            text=self.payload["text"],
            parse_mode="Markdown",
            reply_markup=keyboard,
            protect_content=True,
        )

        return message