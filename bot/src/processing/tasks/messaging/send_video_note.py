from src.processing.tasks.messaging.base_messaging import BaseMessagingTask
from aiogram.types import Message


class SendVideoNoteTask(BaseMessagingTask):

    async def execute(self) -> Message:

        message = await self.bot.send_video_note(
            chat_id=self.payload["user_id"],
            video_note=self.payload["file_id"],
            protect_content=True,
        )

        return message