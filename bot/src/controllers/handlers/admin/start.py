from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.filters import Command

from . import admin_router

@admin_router.message(Command("admin"))
async def start(message: Message, state: FSMContext):
    """Главное меню"""
    await state.clear()

    buttons = [
        [InlineKeyboardButton(text="➕ Добавить файл", callback_data="admin_add_file")],
        [InlineKeyboardButton(text="📋 Список файлов", callback_data="admin_list_files")],
        [InlineKeyboardButton(text="🗑️ Удалить файл", callback_data="admin_delete_file")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(
        "👋 Админка\n\n"
        "Выбери действие:",
        reply_markup=keyboard
    )