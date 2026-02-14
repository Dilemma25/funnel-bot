from src.processing.tasks.messaging.base_messaging import BaseMessagingTask
from aiogram.types import Message


class SendVideoTask(BaseMessagingTask):

    async def execute(self) -> Message:

        message = await self.bot.send_video(
            chat_id=self.payload["user_id"],
            video=self.payload["file_id"],
            protect_content=True,
        )

        return message