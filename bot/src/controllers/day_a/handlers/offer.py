from src.core.logging_config import setup_logging

logger = setup_logging(__name__, service='bot')

from datetime import datetime

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from tortoise.transactions import in_transaction

from src.controllers.day_a.file_codes import FileCodes
from src.controllers.day_a.user_states import DayAStates
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

    file_id = await get_media_by_file_code(FileCodes.VIDEO_NOTE_METHOD, OfferCodesEnum.SMART_WALLET)

    await callback.message.answer_video_note(
        video_note=file_id,
        protect_content=True,
    )

    user_id = callback.from_user.id

    try:
        async with in_transaction() as conn:

            now = datetime.now(settings.timezone)

            # ===== ТАСКА 1: Установка скидки + оффер =====
            # payload_offer = {
            #     "user_id": user_id,
            #     "text": messages.message_A9,
            #     "keyboard": [
            #         [{"text": f"Забрать за {consts.DAY_A_DISCOUNT_PRICE} ₽", "callback_data": "day_a:a9:buy"}],
            #         [{"text": "Узнать подробнее", "callback_data": "day_a:a9:faq"}],
            #     ],
            #     # Параметры скидки
            #     "offer_code": OfferCodesEnum.SMART_WALLET,
            #     "discount_price": consts.DAY_A_DISCOUNT_PRICE,
            #     "discount_duration": Timings.DISCOUNT_TIMER.total_seconds(),
            # }

            payload_offer = SetDiscountTaskPayload(
                user_id=user_id,
                text=messages.message_A9,
                keyboard=keyboard(
                    [button(text=f"Забрать за {consts.DAY_A_DISCOUNT_PRICE} ₽", callback_data="day_a:a9:buy")],
                    [button(text="Узнать подробнее", callback_data="day_a:a9:faq")]
                ),
                offer_code=OfferCodesEnum.SMART_WALLET,
                discount_price=consts.DAY_A_DISCOUNT_PRICE,
                discount_duration=Timings.DISCOUNT_TIMER.total_seconds()
            )

            await create_task(
                user_id=user_id,
                task_type=TaskTypeEnum.SET_DISCOUNT_AND_SEND_MESSAGE,
                payload=payload_offer,
                run_at=now + Timings.OFFER_DELAY,
                connection=conn
            )

            # ===== ТАСКА 2: Напоминание о таймере =====
            # payload_reminder = {
            #     "user_id": user_id,
            #     "text": messages.message_A9_1_1,
            #     "keyboard": [
            #         [{"text": f"💳 Оплатить {consts.DAY_A_DISCOUNT_PRICE} ₽", "callback_data": "day_a:a9:buy"}],
            #     ],
            # }

            payload_reminder = MessageTaskPayload(
                user_id=user_id,
                text=messages.message_A9_1_1,
                keyboard=keyboard(
                    [button(text=f"💳 Оплатить {consts.DAY_A_DISCOUNT_PRICE} ₽", callback_data="day_a:a9:buy")]
                )
            )

            await create_task(
                user_id=user_id,
                task_type=TaskTypeEnum.SEND_MESSAGE,
                payload=payload_reminder,
                run_at=now + Timings.REMEMBER_ABOUT_DISCOUNT,
                connection=conn
            )

            # ===== ТАСКА 3: Окончание скидки =====
            # payload_timeout = {
            #     "user_id": user_id,
            #     "text": messages.message_A10_FINAL,
            #     "offer_code": OfferCodesEnum.SMART_WALLET,
            #     "keyboard": [
            #         [{"text": "💳 Оплатить 3990 ₽", "callback_data": "day_a:a9:buy"}],
            #     ],
            # }

            payload_timeout = RemoveDiscountTaskPayload(
                user_id=user_id,
                text=messages.message_A10_FINAL,
                offer_code=OfferCodesEnum.SMART_WALLET,
                keyboard=keyboard(
                    [button(text="💳 Оплатить 3990 ₽", callback_data="day_a:a9:buy")]
                )
            )

            await create_task(
                user_id=user_id,
                task_type=TaskTypeEnum.REMOVE_DISCOUNT_AND_SEND_MESSAGE,
                payload=payload_timeout,
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

    await callback.message.answer(
        messages.message_A9_2,
        parse_mode="Markdown",
        protect_content=True,
    )
    await callback.message.answer(
        messages.message_A9_faq_1,
        parse_mode="Markdown",
        protect_content = True,
    )
    await callback.message.answer(
        messages.message_A9_faq_2,
        parse_mode="Markdown",
        protect_content=True,
    )
    await callback.message.answer(
        messages.message_A9_faq_3,
        parse_mode="Markdown",
        protect_content=True,
    )
    await callback.message.answer(
        messages.message_A9_faq_4,
        parse_mode="Markdown",
        protect_content=True,
    )

    async with in_transaction() as conn:

        user_id = callback.from_user.id

        # keyboard_json = [
        #     [{"text": f"✅ Забрать за {consts.DAY_A_DISCOUNT_PRICE} ₽", "callback_data": "day_a:a9_2_1:buy"}],
        #     [{"text": "👁 Посмотреть отзывы", "callback_data": "day_a:a9_2_2:reviews"}],
        # ]
        #
        # payload = {
        #     "user_id": user_id,
        #     "text": messages.message_A9_2_1,
        #     "keyboard": keyboard_json
        # }
        #
        task_type = TaskTypeEnum.SEND_MESSAGE

        payload = MessageTaskPayload(
            user_id=user_id,
            text=messages.message_A9_2_1,
            keyboard=keyboard(
                [button(text=f"✅ Забрать за {consts.DAY_A_DISCOUNT_PRICE} ₽", callback_data="day_a:a9_2_1:buy")],
                [button(text="👁 Посмотреть отзывы", callback_data="day_a:a9_2_2:reviews")]
            )
        )
        time_run = datetime.now(settings.timezone) + Timings.RETURN_TO_OFFER

        await create_task(user_id, task_type, payload, time_run, conn)

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

    for idx, file_code in enumerate(FileCodes.REVIEWS, start=1):
        file_id = await get_media_by_file_code(
            file_code,
            OfferCodesEnum.SMART_WALLET,
        )

        reply_markup = keyboard_A9_2_2 if idx == len(FileCodes.REVIEWS) else None

        await callback.message.answer_photo(
            photo=file_id,
            protect_content=True,
            reply_markup=reply_markup,
        )

    user_id = callback.from_user.id

    await update_user_state(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        last_activity_at=datetime.now(settings.timezone),
        state=DayAStates.DAY_A_9_2_2_REVIEWS_SENT,
    )
