from src.processing.tasks.base import BaseTask
from src.safe_bot import SafeBot

from abc import abstractmethod

from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

class BaseMessagingTask(BaseTask):
    """Базовый класс для задач отправки сообщений"""

    def __init__(self, bot: SafeBot, payload: dict):
        self.bot = bot
        self.payload = payload

    def _build_keyboard(self) -> InlineKeyboardMarkup | None:
        """
        Парсит клавиатуру из payload

        Формат payload["keyboard"]:
        [
            [{"text": "Кнопка 1", "callback_data": "btn1"}],
            [{"text": "Кнопка 2", "url": "https://..."}],
        ]

        Returns:
            InlineKeyboardMarkup или None если клавиатуры нет
        """
        keyboard_data = self.payload.get("keyboard")

        if not keyboard_data:
            return None

        buttons = []
        for row in keyboard_data:
            button_row = []
            for btn in row:
                # Поддержка разных типов кнопок
                if "callback_data" in btn:
                    button_row.append(
                        InlineKeyboardButton(
                            text=btn["text"],
                            callback_data=btn["callback_data"]
                        )
                    )
                elif "url" in btn:
                    button_row.append(
                        InlineKeyboardButton(
                            text=btn["text"],
                            url=btn["url"]
                        )
                    )

            if button_row:
                buttons.append(button_row)

        return InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None

    @abstractmethod
    async def execute(self):
        pass