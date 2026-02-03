from src.processing.tasks.base import BaseTask
from src.safe_bot import SafeBot


class SendVideNoteTask(BaseTask):

    def __init__(self, bot: SafeBot, payload: dict):
        self.bot = bot
        self.payload = payload

    async def execute(self):
        await self.bot.send_video_note(
            chat_id=self.payload["user_id"],
            video_note=self.payload["file_id"],
            protect_content=True,
        )