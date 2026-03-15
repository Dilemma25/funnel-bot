from datetime import datetime
from datetime import timezone

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup
from aiogram import F
from tortoise.transactions import in_transaction

import src.controllers.funnel_bot.day_b.messages as messages
from src.controllers.schemas.keyboard import keyboard, button
from src.controllers.schemas.task_payloads import MessageTaskPayload
from src.controllers.user_states import DayBStates, DayAStates
from src.models.offer import OfferCodesEnum
from src.models.sent_message import SentMessageTagEnum
from src.models.sent_message import SentMessageDeleteTimings
from src.models.user_history import EventTypeEnum
from src.processing.task_types import TaskTypeEnum
from src.views.sent_message import track_message
from src.views.tasks import create_task
from src.views.user_history import create_user_history
from src.views.user_state.update_user_state import update_user_state

from . import day_b_router
from ..timings import TimingsDayB


@day_b_router.callback_query(F.data.contains("day_b:a6_1:questions"))
async def question_handler(callback: CallbackQuery, state: FSMContext):

    current_kb: InlineKeyboardMarkup | None = callback.message.reply_markup

    if current_kb:
        # Оставляем только кнопку оплаты
        new_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [btn for btn in row if btn.callback_data and "buy" in btn.callback_data]
                for row in current_kb.inline_keyboard
            ]
        )

        await callback.message.edit_reply_markup(reply_markup=new_kb)

    sent_message = await callback.message.answer(
        text = messages.message_B6_1,
        parse_mode="Markdown",
    )

    user_id = callback.from_user.id

    async with in_transaction() as conn:
        payload = {
            "clicked_button": "b5: Есть вопросы(B6.1)"
        }

        await create_user_history(
            user_id=user_id,
            event_type=EventTypeEnum.BUTTON_CLICKED,
            user_stage=DayBStates.B_5_OFFER,
            payload=payload,
            connection=conn
        )

        await track_message(
            user_id=user_id,
            telegram_message_id=sent_message.message_id,
            tag=SentMessageTagEnum.FUNNEL,
            stage=DayBStates.B_6_1_CONTROL_NOT_LIMITS,
            delete_at=datetime.now(timezone.utc) + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayBStates.FINAL,
            connection=conn
        )

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            last_activity_at=datetime.now(timezone.utc),
            state=DayBStates.B_6_1_CONTROL_NOT_LIMITS,
            connection=conn,
        )

        now = datetime.now(timezone.utc)

        # ===== ТАСКА 1: Цена потом(B6.2) =====
        run_at = now + TimingsDayB.B6_1_TO_B6_2

        payload = MessageTaskPayload(
            user_id=user_id,
            text=messages.message_B6_2,
            keyboard=None,
            message_tag=SentMessageTagEnum.FUNNEL,
            message_stage=DayBStates.B_6_2_PRICE_LATER,
            delete_at=run_at + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayBStates.FINAL
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.SEND_MESSAGE,
            payload=payload.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

        # ===== ТАСКА 2: Инвест блок(B6.3) =====
        run_at = now + TimingsDayB.B6_2_TO_B6_3

        payload = MessageTaskPayload(
            user_id=user_id,
            text=messages.message_B6_3,
            keyboard=keyboard(
                [button(text=f"Забрать за 2 490 ₽", callback_data="day_b:b6_3:buy")]
            ),
            message_tag=SentMessageTagEnum.FUNNEL,
            message_stage=DayBStates.B_6_2_PRICE_LATER,
            delete_at=run_at + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayBStates.FINAL
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.SEND_MESSAGE,
            payload=payload.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

