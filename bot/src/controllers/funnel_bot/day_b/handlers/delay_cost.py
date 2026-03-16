from datetime import datetime, timezone

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F
from tortoise.transactions import in_transaction

import src.controllers.funnel_bot.day_b.messages as messages
from src.controllers.funnel_bot.day_b.file_codes import FileCodesDayB
from src.controllers.schemas.keyboard import keyboard, button
from src.controllers.schemas.task_payloads import SetDiscountTaskPayload, DocumentTaskPayload
from src.controllers.schemas.task_payloads import MessageTaskPayload
from src.controllers.schemas.task_payloads import RemoveDiscountTaskPayload
from src.controllers.user_states import DayBStates, DayCStates
from src.core.config import settings
from src.models.offer import OfferCodesEnum
from src.models.sent_message import SentMessageTagEnum, SentMessageDeleteTimings
from src.models.user_history import EventTypeEnum
from src.processing.task_types import TaskTypeEnum
from src.views.media import get_media_by_file_code
from src.views.sent_message import track_message
from src.views.tasks import create_task
from src.views.user_history import create_user_history
from src.controllers.funnel_bot.day_b import consts
from src.controllers.funnel_bot.day_b.timings import TimingsDayB
from src.views.user_state.update_user_state import update_user_state

from . import day_b_router



@day_b_router.callback_query(F.data == "day_b:b3:delay_cost")
async def delay_cost_handler(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_reply_markup(reply_markup=None)

    delay_cost_video = await get_media_by_file_code(
        file_code=FileCodesDayB.TSENA_PROMEDLENIA,
        offer_code=OfferCodesEnum.SMART_WALLET,
    )

    sent_message = await callback.message.answer_video_note(
        video_note=delay_cost_video,
        protect_content=True,
    )

    user_id = callback.from_user.id

    async with in_transaction() as conn:

        now = datetime.now(timezone.utc)
        #
        # await create_user_history(
        #     user_id=user_id,
        #     event_type=EventTypeEnum.STAGE_ENTERED,
        #     user_stage=DayBStates.B_3_VIDEO_NOTE_DELAY_PRICE,
        #     connection=conn
        # )

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            state=DayBStates.B_3_VIDEO_NOTE_DELAY_PRICE,
            last_activity_at=now,
            connection=conn
        )

        await track_message(
            user_id=user_id,
            telegram_message_id=sent_message.message_id,
            tag=SentMessageTagEnum.FUNNEL,
            stage=DayBStates.B_3_VIDEO_NOTE_DELAY_PRICE,
            delete_at=now + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayCStates.C_1_PERSONAL_UPGRADE,
            connection=conn
        )


        #TODO это какая то хуйня, можно сделать так, чтоб просто отправлялось сообщение, и отправлялся файл
        # ===== ТАСКА 1: Последнее предложение(B4) =====

        html_file = await get_media_by_file_code(
            file_code=FileCodesDayB.COURSE_STRUCTURE,
            offer_code=OfferCodesEnum.SMART_WALLET,
        )

        run_at = datetime.now(timezone.utc) + TimingsDayB.B3_TO_B4

        payload = DocumentTaskPayload(
            user_id=user_id,
            text=messages.message_B4,

            # keyboard=keyboard(
            #     [button(text=f"📋 Посмотреть структуру курса", callback_data="day_b:b4:link_course_structure")]
            # ),
            keyboard=None,
            file_id=html_file,
            message_tag=SentMessageTagEnum.FUNNEL,
            message_stage=DayBStates.B_4_LAST_OFFER,
            delete_at=run_at + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayBStates.FINAL
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.SEND_DOCUMENT,
            payload=payload.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

        # ===== ТАСКА 2: Установка скидки + оффер(B5) =====
        run_at = now + TimingsDayB.OFFER_DELAY

        payload_offer = SetDiscountTaskPayload(
            user_id=user_id,
            text=messages.message_B5,
            keyboard=keyboard(
                [button(text=f"Забрать за {consts.DAY_B_DISCOUNT_PRICE} ₽", callback_data="day_b:b5:buy")],
                [button(text="Есть вопросы", callback_data="day_b:a6_1:questions")]
            ),
            offer_code=OfferCodesEnum.SMART_WALLET,
            discount_price=consts.DAY_B_DISCOUNT_PRICE,
            discount_duration=TimingsDayB.DISCOUNT_TIMER.total_seconds(),

            message_tag=SentMessageTagEnum.FUNNEL,
            message_stage=DayBStates.B_5_OFFER,
            delete_at=run_at + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayBStates.FINAL
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.SET_DISCOUNT_AND_SEND_MESSAGE,
            payload=payload_offer.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

        # ===== ТАСКА 3: Напоминание о таймере(B7) =====
        run_at = now + TimingsDayB.DISCOUNT_REMINDER

        payload_reminder = MessageTaskPayload(
            user_id=user_id,
            text=messages.message_B7,
            keyboard=keyboard(
                [button(text=f"Забираю ₽", callback_data="day_b:b7:offer")]
            ),

            message_tag=SentMessageTagEnum.FUNNEL,
            message_stage=DayBStates.B_7_TIMER_REMINDER,
            delete_at=run_at + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayBStates.FINAL
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.SEND_MESSAGE,
            payload=payload_reminder.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

        # ===== ТАСКА 4: Повторное напоминание о таймере(B8) =====
        run_at = now + TimingsDayB.DISCOUNT_FINAL_REMINDER

        payload_reminder = MessageTaskPayload(
            user_id=user_id,
            text=messages.message_B8,
            keyboard=keyboard(
                [button(text=f"Беру полный пакет", callback_data="day_b:b8:buy")]
            ),

            message_tag=SentMessageTagEnum.FUNNEL,
            message_stage=DayBStates.B_7_TIMER_REMINDER,
            delete_at=run_at + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayBStates.FINAL
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.SEND_MESSAGE,
            payload=payload_reminder.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

        # ===== ТАСКА 5: Окончание скидки (B_FINAL) =====
        run_at = now + TimingsDayB.DISCOUNT_TIMER

        payload_timeout = RemoveDiscountTaskPayload(
            user_id=user_id,
            text=messages.message_B_FINAL,
            offer_code=OfferCodesEnum.SMART_WALLET,
            keyboard=keyboard(
                [button(text="💳 Оплатить 3990 ₽", callback_data="day_b:b_final:buy")]
            ),

            message_tag=SentMessageTagEnum.FUNNEL,
            message_stage=DayBStates.FINAL,
            delete_at=run_at + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayCStates.C_1_PERSONAL_UPGRADE,
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.REMOVE_DISCOUNT_AND_SEND_MESSAGE,
            payload=payload_timeout.model_dump_json(),
            run_at=run_at,
            connection=conn
        )
