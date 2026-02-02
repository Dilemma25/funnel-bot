from . import day_a_router
from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from src.controllers.handlers.day_a import messages as messages
from src.keyboards import day_a_keyboards as day_a_keyboards
from src.states.day_a import DayAStates


@day_a_router.callback_query(
    StateFilter(DayAStates.waiting_for_checklist_choice),
    F.data == "day_a:a3:found"
)
async def handle_found_problems(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        text=messages.message_C1,
        reply_markup=day_a_keyboards.keyboard_quiz_1,
    )

    await state.update_data(quiz_sum=0)
    await state.set_state(DayAStates.quiz_q1)

@day_a_router.callback_query(
    StateFilter(DayAStates.waiting_for_checklist_choice),
    F.data == "day_a:a3:not_found"
)
async def handle_not_found_problems(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        text=messages.message_C2,
        reply_markup=day_a_keyboards.keyboard_quiz_1,
    )

    await state.update_data(quiz_sum=0)
    await state.set_state(DayAStates.quiz_q1)