from src.processing.tasks.messaging.base_messaging import BaseMessagingTask


class SendMessageTask(BaseMessagingTask):
    async def execute(self):

        await self.bot.send_message(
            chat_id=self.payload["user_id"],
            text=self.payload["text"],
            parse_mode="Markdown",
        )