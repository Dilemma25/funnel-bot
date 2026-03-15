from datetime import datetime
from datetime import timezone

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram import F
from tortoise.transactions import in_transaction

import src.controllers.funnel_bot.day_c.messages as messages
import src.controllers.funnel_bot.day_c.consts as consts
from src.controllers.schemas.task_payloads import RemoveDiscountTaskPayload, FinishFunnelTaskPayload
from src.controllers.user_states import DayCStates
from src.models.offer import OfferCodesEnum
from src.models.sent_message import SentMessageTagEnum
from src.models.sent_message import SentMessageDeleteTimings
from src.models.user_history import EventTypeEnum
from src.processing.task_types import TaskTypeEnum
from src.views.sent_message import track_message
from src.views.tasks import create_task
from src.views.tasks.cancel_user_tasks import cancel_user_tasks
from src.views.user_history import create_user_history
from src.views.user_offer import set_discount
from src.views.user_state.update_user_state import update_user_state
from src.controllers.funnel_bot.day_c.timings import TimingsDayC

from . import day_c_router


@day_c_router.callback_query(F.data.contains("day_c:c2:offer"))
async def delay_cost_handler(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_reply_markup(reply_markup=None)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Забрать за 1990 ₽", callback_data="day_b:b5:buy")],
        ]
    )

    user_id = callback.from_user.id

    now = datetime.now(timezone.utc)

    async with in_transaction() as conn:
        # Удаление тасок для юзера
        # в частности удаление таски на окончание воронки, чтоб она не закончилась во время скидки
        await cancel_user_tasks(
            user_id=user_id,
            connection=conn
        )

        await set_discount(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            discount_price=consts.DAY_C_DISCOUNT_PRICE,
            discount_duration=TimingsDayC.DISCOUNT_TIMER.total_seconds(),
            connection=conn
        )

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            state=DayCStates.C_2_OFFER,
            last_activity_at=datetime.now(timezone.utc),
            connection=conn
        )

        # await create_user_history(
        #     user_id=user_id,
        #     event_type=EventTypeEnum.STAGE_ENTERED,
        #     user_stage=DayCStates.C_2_OFFER,
        #     connection=conn
        # )

        # ===== ТАСКА 1: Окончание скидки (C3)=====
        run_at = now + TimingsDayC.DISCOUNT_TIMER

        payload = FinishFunnelTaskPayload(
            user_id=user_id,
            text=messages.message_c3,
            keyboard=None,
            offer_code=OfferCodesEnum.SMART_WALLET,
            message_stage=DayCStates.FINAL,
            message_tag=SentMessageTagEnum.FUNNEL,
            delete_on_stage=DayCStates.FINAL,
            delete_at=run_at + SentMessageDeleteTimings.get_short(),
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.FINISH_FUNNEL,
            payload=payload.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

    sent_message = await callback.message.answer(
        text = messages.message_c2,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

    await track_message(
        user_id=user_id,
        telegram_message_id=sent_message.message_id,
        tag=SentMessageTagEnum.FUNNEL,
        stage=DayCStates.C_2_OFFER,
        delete_at=now + SentMessageDeleteTimings.get_default(),
        delete_on_stage=DayCStates.FINAL
    )

