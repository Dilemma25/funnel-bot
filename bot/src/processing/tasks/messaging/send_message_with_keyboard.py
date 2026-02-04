from src.processing.tasks.messaging.base_messaging import BaseMessagingTask
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


class SendMessageWithKeyboardTask(BaseMessagingTask):

    async def execute(self):

        keyboard_data = self.payload.get("keyboard")

        keyboard = None

        if keyboard_data:
            buttons = []
            for row in keyboard_data:
                button_row = []
                for btn in row:
                    button_row.append(
                        InlineKeyboardButton(
                            text=btn["text"],
                            callback_data=btn["callback_data"]
                        )
                    )
                buttons.append(button_row)
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            print(f"DEBUG TaskExecute: keyboard created = {keyboard}")  # ← Дебаг

        await self.bot.send_message(
            chat_id=self.payload["user_id"],
            text=self.payload["text"],
            reply_markup=keyboard,
            parse_mode="Markdown",
        )