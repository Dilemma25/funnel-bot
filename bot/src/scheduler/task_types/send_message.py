from src.scheduler.task_types.base import BaseTask
from src.safe_bot import SafeBot


class SendMessageTask(BaseTask):

    def __init__(self, bot: SafeBot, payload: dict):
        self.bot = bot
        self.payload = payload

    async def execute(self):
        await self.bot.send_message(
            chat_id=self.payload["user_id"],
            text=self.payload["text"],
            parse_mode="html"
        )