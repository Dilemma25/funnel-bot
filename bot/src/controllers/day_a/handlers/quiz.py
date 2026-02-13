from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from tortoise.transactions import in_transaction

from src.keyboards import day_a_keyboards as day_a_keyboards
from src.models.offer import OfferCodesEnum
from src.controllers.day_a.consts import QUIZ_ANSWERS
from src.processing.task_types import TaskTypeEnum
from src.views.media import get_media_by_file_code
from src.views.tasks import create_task
from src.controllers.day_a import messages as messages
from src.views.user_state.update_user_state import update_user_state
from . import day_a_router

from datetime import datetime

from src.controllers.day_a.timings import Timings
from ..file_codes import FileCodes
from src.core.config import settings
from ..user_states import DayAStates

from src.controllers.schemas.task_payloads import VideoNoteTaskPayload
from src.controllers.schemas.task_payloads import MessageTaskPayload

from src.controllers.schemas.keyboard import keyboard
from src.controllers.schemas.keyboard import button

@day_a_router.callback_query(
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

    user_id = callback.from_user.id

    await update_user_state(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        last_activity_at=datetime.now(settings.timezone),
        state=DayAStates.A_4_QUIZ_Q1,
    )


@day_a_router.callback_query(
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

    user_id = callback.from_user.id

    await update_user_state(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        last_activity_at=datetime.now(settings.timezone),
        state=DayAStates.A_4_QUIZ_Q2,
    )

@day_a_router.callback_query(
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

    user_id = callback.from_user.id

    await update_user_state(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        last_activity_at=datetime.now(settings.timezone),
        state=DayAStates.A_4_QUIZ_Q2
    )

@day_a_router.callback_query(
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

    user_id = callback.from_user.id

    await update_user_state(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        last_activity_at=datetime.now(settings.timezone),
        state=DayAStates.A_4_QUIZ_Q3
    )

@day_a_router.callback_query(
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

    user_id = callback.from_user.id

    await update_user_state(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        last_activity_at=datetime.now(settings.timezone),
        state=DayAStates.A_4_QUIZ_Q4
    )

@day_a_router.callback_query(
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

    await state.update_data(quiz_sum=None)

    async with in_transaction() as conn:

        #Таска на кружок(A6)
        user_id = callback.from_user.id
        file_id = await get_media_by_file_code(FileCodes.VIDEO_NOTE_JADNOST, OfferCodesEnum.SMART_WALLET)

        task_type = TaskTypeEnum.SEND_VIDEO_NOTE

        payload = VideoNoteTaskPayload(
            user_id=user_id,
            file_id=file_id,
        )

        time_run = datetime.now(settings.timezone) + Timings.VIDEO_NOTE_DELAY
        # payload = {
        #     "user_id": user_id,
        #     "file_id": file_id
        # }
        #
        # task_type = "send_video_note"
        # time_run = datetime.now(settings.timezone) + Timings.VIDEO_NOTE_DELAY

        await create_task(user_id, task_type, payload, time_run, conn)

        #Таска на переход после кружка
        # keyboard_json = [
        #     [{"text": "Понятно, что дальше?", "callback_data": "day_a:a7:next"}],
        # ]
        #
        # payload = {
        #     "user_id": user_id,
        #     "text": messages.message_A7,
        #     "keyboard" : keyboard_json
        # }
        #
        # task_type = "send_message"

        task_type = TaskTypeEnum.SEND_MESSAGE

        payload = MessageTaskPayload(
            user_id=user_id,
            text=messages.message_A7,
            keyboard=keyboard(
                [button(text="Понятно, что дальше?", callback_data="day_a:a7:next")]
            )
        )
        time_run = datetime.now(settings.timezone) + Timings.SYSTEM_MESSAGE_DELAY

        await create_task(user_id, task_type, payload, time_run, conn)

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            last_activity_at=datetime.now(settings.timezone),
            state=DayAStates.A_5_QUIZ_RESULT_SENT,
            connection=conn,
        )

