from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from src.controllers.smart_wallet_course.handlers import smart_wallet_router

@smart_wallet_router.message(Command("menu"))
async def menu(message: Message):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="▸ Урок 1",
            callback_data="lesson_1"
        )]
    ])

    await message.answer(
        text="Выберите урок",
        reply_markup=keyboard
    )