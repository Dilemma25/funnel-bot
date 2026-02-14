from src.processing.tasks.messaging.base_messaging import BaseMessagingTask
from aiogram.types import Message


class SendDocumentTask(BaseMessagingTask):

    async def execute(self) -> Message:

        message = await self.bot.send_document(
            chat_id=self.payload["user_id"],
            caption=self.payload["text"],
            parse_mode="Markdown",
            document=self.payload["file_id"],
            protect_content=True,
        )

        return message