from src.processing.tasks.messaging.base_messaging import BaseMessagingTask


class SendDocumentTask(BaseMessagingTask):

    async def execute(self):

        await self.bot.send_document(
            chat_id=self.payload["user_id"],
            caption=self.payload["text"],
            parse_mode="Markdown",
            document=self.payload["file_id"],
            protect_content=True,
        )