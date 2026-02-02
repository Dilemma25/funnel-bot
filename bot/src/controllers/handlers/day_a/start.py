from aiogram import F
from aiogram.filters import CommandStart
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery

from src.keyboards.day_a_keyboards import keyboard_A1
from src.views.user import get_or_create_user
from src.views.media import get_by_file_name
from src.views.tasks import create
from src.states.day_a import DayAStates
import src.controllers.handlers.day_a.messages as messages
from . import day_a_router
from src.core.config import config

from datetime import datetime
from datetime import timedelta


@day_a_router.message(CommandStart())
async def start_day_a(message: Message, state: FSMContext):
    await get_or_create_user(message.from_user.id)

    await message.answer(
        messages.message_A1,
        parse_mode="Markdown",
        reply_markup=keyboard_A1,
    )

    await state.set_state(DayAStates.starting_day_a)


@day_a_router.callback_query(
    StateFilter(DayAStates.starting_day_a),
    F.data == "day_a:a1:start"
)
async def send_video_lid(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    file_id = await get_by_file_name("test_big")

    await callback.message.answer_video(
        video=file_id,
        caption=messages.message_A2,
        protect_content=True,
        parse_mode="Markdown",
    )

    task_type = "send_document"
    file_id = await get_by_file_name("test_pdf")

    user_id = callback.message.chat.id

    payload = {
        "user_id": user_id,
        "text": messages.message_A3,
        "file_id": file_id
    }

    time_run = datetime.now(config["TIMEZONE"]) + timedelta(seconds=30)

    await create(user_id, task_type, payload, time_run)

    # Таска с клавиатурой
    keyboard_json = [
        [{"text": "Нашёл(ла) несколько пунктов про себя", "callback_data": "day_a:a3:found"}],
        [{"text": "Пока не вижу явных проблем", "callback_data": "day_a:a3:not_found"}],
    ]

    payload = {
        "user_id": user_id,
        "text": messages.message_A3_kb,
        "keyboard": keyboard_json
    }
    time_run = datetime.now(config["TIMEZONE"]) + timedelta(seconds=60)
    await create(user_id, "send_message_with_keyboard", payload, time_run)

    await state.set_state(DayAStates.waiting_for_checklist_choice)

