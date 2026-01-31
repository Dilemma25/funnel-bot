import datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.views.get_or_create_user import get_or_create_user
from src.states.day_a import DayAStates
import src.controllers.handlers.day_a.messages as messages

day_a_router = Router()

@day_a_router.message(CommandStart())
async def start_day_a(message: Message, state: FSMContext):
    await get_or_create_user(message.from_user.id)

    await state.update_data(
        telegram_id=message.from_user.id,
        day_a_started = datetime.datetime.now().isoformat()
    )

    await message.answer(messages.message_A1, parse_mode="Markdown")

    await state.set_state(DayAStates())