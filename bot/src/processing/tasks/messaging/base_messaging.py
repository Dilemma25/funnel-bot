from src.processing.tasks.base import BaseTask
from src.safe_bot import SafeBot
from abc import abstractmethod


class BaseMessagingTask(BaseTask):
    """Базовый класс для задач отправки сообщений"""

    def __init__(self, bot: SafeBot, payload: dict):
        self.bot = bot
        self.payload = payload

    @abstractmethod
    async def execute(self):
        pass