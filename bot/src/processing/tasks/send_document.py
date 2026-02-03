from src.processing.tasks.base import BaseTask
from src.safe_bot import SafeBot


class SendDocumentTask(BaseTask):

    def __init__(self, bot: SafeBot, payload: dict):
        self.bot = bot
        self.payload = payload

    async def execute(self):
        await self.bot.send_document(
            chat_id=self.payload["user_id"],
            caption=self.payload["text"],
            parse_mode="Markdown",
            document=self.payload["file_id"],
            protect_content=True,
        )