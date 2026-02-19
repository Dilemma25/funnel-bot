from src.controllers.common_states import CommonStates
from src.core.logging_config import setup_logging
from src.models.user_history import EventTypeEnum
from src.views.sent_message import track_message
from src.views.user_history import create_user_history

logger = setup_logging(__name__, service='funnel_bot')

from datetime import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from tortoise.transactions import in_transaction

from src.models.sent_message import SentMessageTagEnum
from src.models.sent_message import SentMessageDeleteTimings
from src.controllers.day_a.file_codes import FileCodes
from src.controllers.user_states import DayAStates, DayBStates
from src.models.offer import OfferCodesEnum
from src.controllers.day_a import messages
from src.controllers.day_a.handlers import day_a_router
from src.controllers.day_a.timings import Timings
from src.core.config import settings
from src.keyboards.day_a_keyboards import keyboard_A9_2_2
from src.processing.task_types import TaskTypeEnum
from src.views.media import get_media_by_file_code
from src.views.tasks import create_task
from src.views.user_state.update_user_state import update_user_state
from src.controllers.day_a import consts as consts

from src.controllers.schemas.keyboard import keyboard
from src.controllers.schemas.keyboard import button

from src.controllers.schemas.task_payloads import SetDiscountTaskPayload
from src.controllers.schemas.task_payloads import MessageTaskPayload
from src.controllers.schemas.task_payloads import RemoveDiscountTaskPayload


@day_a_router.callback_query(F.data == "day_a:a7:next")
async def handle_a7_next(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_reply_markup(reply_markup=None)

    user_id = callback.from_user.id

    file_id = await get_media_by_file_code(FileCodes.VIDEO_NOTE_METHOD, OfferCodesEnum.SMART_WALLET)

    message = await callback.message.answer_video_note(
        video_note=file_id,
        protect_content=True,
    )

    try:
        async with in_transaction() as conn:

            await track_message(
                user_id=user_id,
                telegram_message_id=message.message_id,
                tag=SentMessageTagEnum.FUNNEL,
                stage=DayAStates.A_8_VIDEO_NOTE_METHOD_SENT,
                delete_at=datetime.now(settings.timezone) + SentMessageDeleteTimings.get_long(),
                delete_on_stage=DayAStates.FINAL,
                connection=conn
            )

            now = datetime.now(settings.timezone)

            # ===== ТАСКА 1: Установка скидки + оффер =====
            payload_offer = SetDiscountTaskPayload(
                user_id=user_id,
                text=messages.message_A9,
                keyboard=keyboard(
                    [button(text=f"Забрать за {consts.DAY_A_DISCOUNT_PRICE} ₽", callback_data="day_a:a9:buy")],
                    [button(text="Узнать подробнее", callback_data="day_a:a9:faq")]
                ),
                offer_code=OfferCodesEnum.SMART_WALLET,
                discount_price=consts.DAY_A_DISCOUNT_PRICE,
                discount_duration=Timings.DISCOUNT_TIMER.total_seconds(),

                message_tag=SentMessageTagEnum.FUNNEL,
                message_stage=DayAStates.A_9_OFFER_SENT,
                delete_at=datetime.now(settings.timezone) + SentMessageDeleteTimings.get_default(),
                delete_on_stage=DayAStates.FINAL
            )

            await create_task(
                user_id=user_id,
                task_type=TaskTypeEnum.SET_DISCOUNT_AND_SEND_MESSAGE,
                payload=payload_offer.model_dump_json(),
                run_at=now + Timings.OFFER_DELAY,
                connection=conn
            )

            # ===== ТАСКА 2: Напоминание о таймере =====

            payload_reminder = MessageTaskPayload(
                user_id=user_id,
                text=messages.message_A9_1_1,
                keyboard=keyboard(
                    [button(text=f"💳 Оплатить {consts.DAY_A_DISCOUNT_PRICE} ₽", callback_data="day_a:a9:buy")]
                ),

                message_tag=SentMessageTagEnum.FUNNEL,
                message_stage=DayAStates.A_9_1_1_REMEMBER_ABOUT_DISCOUNT,
                delete_at=datetime.now(settings.timezone) + SentMessageDeleteTimings.get_default(),
                delete_on_stage=DayAStates.FINAL
            )

            await create_task(
                user_id=user_id,
                task_type=TaskTypeEnum.SEND_MESSAGE,
                payload=payload_reminder.model_dump_json(),
                run_at=now + Timings.REMEMBER_ABOUT_DISCOUNT,
                connection=conn
            )

            # ===== ТАСКА 3: Окончание скидки =====

            payload_timeout = RemoveDiscountTaskPayload(
                user_id=user_id,
                text=messages.message_A10_FINAL,
                offer_code=OfferCodesEnum.SMART_WALLET,
                keyboard=keyboard(
                    [button(text="💳 Оплатить 3990 ₽", callback_data="day_a:a9:buy")]
                ),

                message_tag = SentMessageTagEnum.FUNNEL,
                message_stage = CommonStates.DISCOUNT_EXPIRES,
                delete_at = datetime.now(settings.timezone) + SentMessageDeleteTimings.get_default(),
                delete_on_stage = DayBStates.B_1_COLD_SHOWER,
            )

            await create_task(
                user_id=user_id,
                task_type=TaskTypeEnum.REMOVE_DISCOUNT_AND_SEND_MESSAGE,
                payload=payload_timeout.model_dump_json(),
                run_at=now + Timings.DISCOUNT_TIMER,
                connection=conn
            )

            await update_user_state(
                user_id=user_id,
                offer_code=OfferCodesEnum.SMART_WALLET,
                last_activity_at=datetime.now(settings.timezone),
                state=DayAStates.A_7_SYSTEM_MESSAGE_SENT,
                connection=conn
            )

    except Exception as e:
        logger.error(f"❌ Ошибка создания тасок: {e}", exc_info=True)
        # await callback.message.answer("Произошла ошибка. Попробуй позже.")


@day_a_router.callback_query(
    F.data == "day_a:a9:faq"
)
async def handle_faq(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

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

    # ✅ Собираем message_id из всех отправленных сообщений
    sent_message_ids = []

    msg1 = await callback.message.answer(
        messages.message_A9_2,
        parse_mode="Markdown",
        protect_content=True,
    )
    sent_message_ids.append(msg1.message_id)

    msg2 = await callback.message.answer(
        messages.message_A9_faq_1,
        parse_mode="Markdown",
        protect_content=True,
    )
    sent_message_ids.append(msg2.message_id)

    msg3 = await callback.message.answer(
        messages.message_A9_faq_2,
        parse_mode="Markdown",
        protect_content=True,
    )
    sent_message_ids.append(msg3.message_id)

    msg4 = await callback.message.answer(
        messages.message_A9_faq_3,
        parse_mode="Markdown",
        protect_content=True,
    )
    sent_message_ids.append(msg4.message_id)

    msg5 = await callback.message.answer(
        messages.message_A9_faq_4,
        parse_mode="Markdown",
        protect_content=True,
    )
    sent_message_ids.append(msg5.message_id)

    user_id = callback.from_user.id

    async with in_transaction() as conn:

        payload = {
            "clicked_button": "a9: Узнать подробнее(A9.1)"
        }

        await create_user_history(
            user_id=user_id,
            event_type=EventTypeEnum.BUTTON_CLICKED,
            user_stage=DayAStates.A_9_OFFER_SENT,
            payload=payload,
            connection=conn
        )

        for message_id in sent_message_ids:
            await track_message(
                user_id=user_id,
                telegram_message_id=message_id,
                tag=SentMessageTagEnum.FUNNEL,
                stage=DayAStates.A_9_2_FAQ_SENT,
                delete_at=datetime.now(settings.timezone) + SentMessageDeleteTimings.get_default(),
                delete_on_stage=DayAStates.FINAL,
                connection=conn
            )

        task_type = TaskTypeEnum.SEND_MESSAGE

        payload = MessageTaskPayload(
            user_id=user_id,
            text=messages.message_A9_2_1,
            keyboard=keyboard(
                [button(text=f"✅ Забрать за {consts.DAY_A_DISCOUNT_PRICE} ₽", callback_data="day_a:a9_2_1:buy")],
                [button(text="👁 Посмотреть отзывы", callback_data="day_a:a9_2_2:reviews")]
            ),

            message_tag=SentMessageTagEnum.FUNNEL,
            message_stage=DayAStates.A_9_2_1_REPEAT_OFFER_SENT,
            delete_at=datetime.now(settings.timezone) + SentMessageDeleteTimings.get_default(),
            delete_on_stage=DayAStates.FINAL,
        )
        time_run = datetime.now(settings.timezone) + Timings.RETURN_TO_OFFER

        await create_task(user_id, task_type, payload.model_dump_json(), time_run, conn)

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            last_activity_at=datetime.now(settings.timezone),
            state=DayAStates.A_9_2_FAQ_SENT,
            connection=conn
        )

@day_a_router.callback_query(
    F.data == "day_a:a9_2_2:reviews"
)
async def handle_reviews(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

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

    user_id = callback.from_user.id

    messages_ids = []

    for idx, file_code in enumerate(FileCodes.REVIEWS, start=1):
        file_id = await get_media_by_file_code(
            file_code,
            OfferCodesEnum.SMART_WALLET,
        )

        reply_markup = keyboard_A9_2_2 if idx == len(FileCodes.REVIEWS) else None

        message = await callback.message.answer_photo(
            photo=file_id,
            protect_content=True,
            reply_markup=reply_markup,
        )

        messages_ids.append(message.message_id)

    async with in_transaction() as conn:

        payload = {
            "clicked_button": "a9_2_2: Отзывы(A9.2.2)"
        }

        await create_user_history(
            user_id=user_id,
            event_type=EventTypeEnum.BUTTON_CLICKED,
            user_stage=DayAStates.A_9_2_FAQ_SENT,
            payload=payload,
            connection=conn
        )

        for message_id in messages_ids:

            await track_message(
                user_id=user_id,
                telegram_message_id=message_id,
                tag=SentMessageTagEnum.FUNNEL,
                stage=DayAStates.A_9_2_2_REVIEWS_SENT,
                delete_at=datetime.now(settings.timezone) + SentMessageDeleteTimings.get_default(),
                delete_on_stage=DayAStates.FINAL,
                connection=conn
            )

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            last_activity_at=datetime.now(settings.timezone),
            state=DayAStates.A_9_2_2_REVIEWS_SENT,
            connection=conn,
        )
