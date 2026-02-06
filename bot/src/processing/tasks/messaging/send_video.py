from src.processing.tasks.messaging.base_messaging import BaseMessagingTask


class SendVideoTask(BaseMessagingTask):

    async def execute(self):

        await self.bot.send_video(
            chat_id=self.payload["user_id"],
            video=self.payload["file_id"],
            protect_content=True,
        )