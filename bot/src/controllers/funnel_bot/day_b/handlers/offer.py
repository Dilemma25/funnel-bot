from datetime import datetime, timezone

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram import F
from tortoise.transactions import in_transaction

import src.controllers.funnel_bot.day_b.messages as messages
from src.controllers.user_states import DayBStates
from src.models.sent_message import SentMessageTagEnum
from src.models.sent_message import SentMessageDeleteTimings
from src.models.user_history import EventTypeEnum
from src.views.sent_message import track_message
from src.views.user_history import create_user_history

from . import day_b_router



@day_b_router.callback_query(F.data.contains("day_b:b7:offer"))
async def delay_cost_handler(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_reply_markup(reply_markup=None)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Забрать за 2 490 ₽", callback_data="day_b:b5:buy")],
        ]
    )

    sent_message = await callback.message.answer(
        text = messages.message_B5,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

    user_id = callback.from_user.id

    async with in_transaction() as conn:

        now = datetime.now(timezone.utc)

        await track_message(
            user_id=user_id,
            telegram_message_id=sent_message.message_id,
            tag=SentMessageTagEnum.FUNNEL,
            stage=DayBStates.B_5_OFFER,
            delete_at=now + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayBStates.FINAL
        )

        payload = {
            "clicked_button": "b7: Забираю ₽(B5)"
        }

        await create_user_history(
            user_id=user_id,
            event_type=EventTypeEnum.BUTTON_CLICKED,
            user_stage=DayBStates.B_6_1_CONTROL_NOT_LIMITS,
            payload=payload,
            connection=conn
        )

