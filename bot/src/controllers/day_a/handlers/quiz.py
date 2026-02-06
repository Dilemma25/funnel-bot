from aiogram import F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from tortoise.transactions import in_transaction

from src.keyboards import day_a_keyboards as day_a_keyboards
from src.models.offer import OfferCodesEnum
from src.states.day_a import DayAStates
from src.controllers.day_a.consts import QUIZ_ANSWERS
from src.views.media import get_media_by_file_code
from src.views.tasks import create_task
from src.core.config import config
from src.controllers.day_a import messages as messages
from . import day_a_router

from datetime import datetime

from src.controllers.day_a.timings import Timings


@day_a_router.callback_query(
    StateFilter(DayAStates.a_2_video_sent),
    F.data.startswith("day_a:a3:found")
)
async def handle_found_problems(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.delete()

    await callback.message.answer(
        text=messages.message_C1,
        parse_mode="Markdown",
        protect_content=True,
    )

    await callback.message.answer(
        text=messages.message_A4_q1,
        reply_markup=day_a_keyboards.keyboard_quiz_1,
        parse_mode="Markdown",
        protect_content=True,
    )

    await state.update_data(
        quiz_sum=0,
    )
    await state.set_state(DayAStates.a_4_quiz_q1)

@day_a_router.callback_query(
    StateFilter(DayAStates.a_2_video_sent),
    F.data.startswith("day_a:a3:not_found")
)
async def handle_not_found_problems(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.delete()

    await callback.message.answer(
        text=messages.message_C2,
        parse_mode="Markdown",
        protect_content=True,
    )

    await callback.message.answer(
        text=messages.message_A4_q1,
        reply_markup=day_a_keyboards.keyboard_quiz_1,
        parse_mode="Markdown",
        protect_content=True,
    )

    await state.update_data(
        quiz_sum=0,
    )
    await state.set_state(DayAStates.a_4_quiz_q1)

@day_a_router.callback_query(
    StateFilter(DayAStates.a_4_quiz_q1),
    F.data.startswith("day_a:a4:q1_")
)
async def handle_quiz_1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.delete()

    await callback.message.answer(
        text=messages.message_A4_q2,
        reply_markup=day_a_keyboards.keyboard_quiz_2,
        parse_mode="Markdown",
        protect_content=True,
    )

    answer_q1 = callback.data.split("_")[-1]
    price = QUIZ_ANSWERS["q1"][answer_q1]

    data = await state.get_data()

    data["quiz_sum"] += price
    await state.update_data(quiz_sum=data["quiz_sum"])

    await state.set_state(DayAStates.a_4_quiz_q2)

@day_a_router.callback_query(
    StateFilter(DayAStates.a_4_quiz_q2),
    F.data.startswith("day_a:a4:q2_")
)
async def handle_quiz_2(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.delete()

    await callback.message.answer(
        text=messages.message_A4_q3,
        reply_markup=day_a_keyboards.keyboard_quiz_3,
        parse_mode="Markdown",
        protect_content=True,
    )

    answer_q2 = callback.data.split("_")[-1]
    price = QUIZ_ANSWERS["q2"][answer_q2]

    data = await state.get_data()
    data["quiz_sum"] += price
    await state.update_data(quiz_sum=data["quiz_sum"])

    await state.set_state(DayAStates.a_4_quiz_q3)

@day_a_router.callback_query(
    StateFilter(DayAStates.a_4_quiz_q3),
    F.data.startswith("day_a:a4:q3_")
)
async def handle_quiz_3(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.delete()

    await callback.message.answer(
        text=messages.message_A4_q4,
        reply_markup=day_a_keyboards.keyboard_quiz_4,
        parse_mode="Markdown",
        protect_content=True,
    )

    answer_q3 = callback.data.split("_")[-1]
    price = QUIZ_ANSWERS["q3"][answer_q3]

    data = await state.get_data()
    data["quiz_sum"] += price
    await state.update_data(quiz_sum=data["quiz_sum"])

    await state.set_state(DayAStates.a_4_quiz_q4)

@day_a_router.callback_query(
    StateFilter(DayAStates.a_4_quiz_q4),
    F.data.startswith("day_a:a4:q4_")
)
async def handle_quiz_4(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.delete()

    answer_q4 = callback.data.split("_")[-1]
    price = QUIZ_ANSWERS["q4"][answer_q4]

    data = await state.get_data()
    final_sum = data.get("quiz_sum", 0) + price

    await callback.message.answer(
        text=messages.create_quiz_result_message(final_sum),
        parse_mode="Markdown",
        protect_content=True,
    )

    offer_id = await state.get_value("offer_id")

    async with in_transaction() as conn:

        #Таска на кружок(A6)
        user_id = callback.from_user.id
        file_id = await get_media_by_file_code("V1_krujok_jadnost", offer_id)

        payload = {
            "user_id": user_id,
            "file_id": file_id
        }

        task_type = "send_video_note"
        time_run = datetime.now(config["TIMEZONE"]) + Timings.VIDEO_NOTE_DELAY

        await create_task(user_id, task_type, payload, time_run, conn)

        keyboard_json = [
            [{"text": "Понятно, что дальше?", "callback_data": "day_a:a7:next"}],
        ]

        payload = {
            "user_id": user_id,
            "text": messages.message_A7,
            "keyboard" : keyboard_json
        }

        task_type = "send_message_with_keyboard"
        time_run = datetime.now(config["TIMEZONE"]) + Timings.SYSTEM_MESSAGE_DELAY

        await create_task(user_id, task_type, payload, time_run, conn)

    await state.set_state(DayAStates.a_5_quiz_result_sent)

