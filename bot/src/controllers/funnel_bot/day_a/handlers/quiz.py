from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from tortoise.transactions import in_transaction

from src.keyboards import day_a_keyboards as day_a_keyboards
from src.models.offer import OfferCodesEnum
from src.controllers.funnel_bot.day_a.consts import QUIZ_ANSWERS
from src.models.sent_message import SentMessageDeleteTimings, SentMessageTagEnum
from src.models.user_history import EventTypeEnum
from src.processing.task_types import TaskTypeEnum
from src.views.media import get_media_by_file_code
from src.views.sent_message import track_message
from src.views.tasks import create_task
from .. import messages as messages
from src.views.user_history import create_user_history
from src.views.user_state.update_user_state import update_user_state
from . import day_a_router

from datetime import datetime, timezone

from src.controllers.funnel_bot.day_a.timings import Timings
from ..file_codes import FileCodes
from src.core.config import settings
from src.controllers.user_states import DayAStates

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

    user_id = callback.from_user.id

    message = await callback.message.answer(
        text=messages.message_C1,
        parse_mode="Markdown",
        protect_content=True,
    )
    async with in_transaction() as conn:

        await track_message(
            user_id=user_id,
            telegram_message_id=message.message_id,
            tag=SentMessageTagEnum.FUNNEL,
            stage=DayAStates.C1_FOUND_SENT,
            delete_at=datetime.now(settings.timezone) + SentMessageDeleteTimings.get_long(),
            delete_on_stage=DayAStates.FINAL,
            connection=conn
        )

        payload = {
            "clicked_button": "a3: Нашёл(ла) несколько пунктов про себя(A3.1)"
        }

        await create_user_history(
            user_id=user_id,
            event_type=EventTypeEnum.BUTTON_CLICKED,
            user_stage=DayAStates.A_3_CHECKLIST_SENT,
            payload=payload,
            connection=conn
        )

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            last_activity_at=datetime.now(settings.timezone),
            state=DayAStates.A_4_QUIZ_Q1,
            connection=conn
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


@day_a_router.callback_query(
    F.data.startswith("day_a:a3:not_found")
)
async def handle_not_found_problems(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.delete()

    user_id = callback.from_user.id

    message = await callback.message.answer(
        text=messages.message_C2,
        parse_mode="Markdown",
        protect_content=True,
    )
    async with in_transaction() as conn:

        await track_message(
            user_id=user_id,
            telegram_message_id=message.message_id,
            tag=SentMessageTagEnum.FUNNEL,
            stage=DayAStates.C2_NOT_FOUND_SENT,
            delete_at=datetime.now(settings.timezone) + SentMessageDeleteTimings.get_long(),
            delete_on_stage=DayAStates.FINAL,
            connection=conn
        )

        payload = {
            "clicked_button": "a3: Пока не вижу явных проблем(A3.1)"
        }

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            last_activity_at=datetime.now(settings.timezone),
            state=DayAStates.A_4_QUIZ_Q1,
            connection=conn
        )

        await create_user_history(
            user_id=user_id,
            event_type=EventTypeEnum.BUTTON_CLICKED,
            user_stage=DayAStates.A_3_CHECKLIST_SENT,
            payload=payload,
            connection=conn
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

    user_id = callback.from_user.id

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

        # await create_user_history(
        #     user_id=user_id,
        #     event_type=EventTypeEnum.STAGE_ENTERED,
        #     user_stage=DayAStates.A_3_CHECKLIST_SENT,
        #     connection=conn
        # )

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            last_activity_at=datetime.now(settings.timezone),
            state=DayAStates.A_5_QUIZ_RESULT_SENT,
            connection=conn,
        )

        now = datetime.now(timezone.utc)
        # ===== ТАСКА 1: КРУЖОК 1 "КОНТРОЛЬ ≠ ЖАДНОСТЬ" (А6) =====
        run_at = now + Timings.VIDEO_NOTE_DELAY

        file_id = await get_media_by_file_code(FileCodes.VIDEO_NOTE_JADNOST, OfferCodesEnum.SMART_WALLET)

        payload = VideoNoteTaskPayload(
            user_id=user_id,
            file_id=file_id,

            message_tag=SentMessageTagEnum.FUNNEL,
            message_stage=DayAStates.A_6_VIDEO_NOTE_JADNOST_SENT,
            delete_at=run_at + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayAStates.FINAL
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.SEND_VIDEO_NOTE,
            payload=payload.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

        # ===== ТАСКА 2: АНАЛОГИЯ + ФОРМУЛА (А7) =====
        run_at = now + Timings.SYSTEM_MESSAGE_DELAY

        payload = MessageTaskPayload(
            user_id=user_id,
            text=messages.message_A7,
            keyboard=keyboard(
                [button(text="Понятно, что дальше?", callback_data="day_a:a7:next")]
            ),
            message_tag=SentMessageTagEnum.FUNNEL,
            message_stage=DayAStates.A_7_SYSTEM_MESSAGE_SENT,
            delete_at=run_at + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayAStates.FINAL
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.SEND_MESSAGE,
            payload=payload.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

