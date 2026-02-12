from datetime import datetime
import logging

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from tortoise.transactions import in_transaction

from src.controllers.day_a.file_codes import FileCodes
from src.controllers.day_a.user_states import DayAStates
from src.models.offer import OfferCodesEnum
from src.controllers.day_a import messages
from src.controllers.day_a.handlers import day_a_router
from src.controllers.day_a.timings import Timings
from src.core.config import config
from src.core.config import settings
from src.keyboards.day_a_keyboards import keyboard_A9_2_2
from src.views.media import get_media_by_file_code
from src.views.tasks import create_task
from src.views.user_state.update_user_state import update_user_state
from src.controllers.day_a import consts as consts


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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
            offer_code = OfferCodesEnum.SMART_WALLET

            # ===== ТАСКА 1: Установка скидки + оффер =====
            payload_offer = {
                "user_id": user_id,
                "text": messages.message_A9,
                "keyboard": [
                    [{"text": f"Забрать за {consts.DAY_A_DISCOUNT_PRICE} ₽", "callback_data": "day_a:a9:buy"}],
                    [{"text": "Узнать подробнее", "callback_data": "day_a:a9:faq"}],
                ],
                # Параметры скидки
                "offer_code": offer_code,
                "discount_price": consts.DAY_A_DISCOUNT_PRICE,
                "discount_duration": Timings.DISCOUNT_TIMER.total_seconds(),
            }

            await create_task(
                user_id=user_id,
                task_type="set_discount_and_send_message_task",
                payload=payload_offer,
                run_at=now + Timings.OFFER_DELAY,
                connection=conn
            )

            # ===== ТАСКА 2: Напоминание о таймере =====
            payload_reminder = {
                "user_id": user_id,
                "text": messages.message_A9_1_1,
                "keyboard": [
                    [{"text": f"💳 Оплатить {consts.DAY_A_DISCOUNT_PRICE} ₽", "callback_data": "day_a:a9:buy"}],
                ],
            }

            await create_task(
                user_id=user_id,
                task_type="send_message",
                payload=payload_reminder,
                run_at=now + Timings.REMEMBER_ABOUT_DISCOUNT,
                connection=conn
            )

            # ===== ТАСКА 3: Окончание скидки =====
            payload_timeout = {
                "user_id": user_id,
                "text": messages.message_A10_FINAL,
                "offer_code": offer_code,
                "keyboard": [
                    [{"text": "💳 Оплатить 3990 ₽", "callback_data": "day_a:a9:buy"}],
                ],
            }

            await create_task(
                user_id=user_id,
                task_type="remove_discount_and_send_message_task",
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

        keyboard_json = [
            [{"text": f"✅ Забрать за {consts.DAY_A_DISCOUNT_PRICE} ₽", "callback_data": "day_a:a9_2_1:buy"}],
            [{"text": "👁 Посмотреть отзывы", "callback_data": "day_a:a9_2_2:reviews"}],
        ]

        payload = {
            "user_id": user_id,
            "text": messages.message_A9_2_1,
            "keyboard": keyboard_json
        }

        task_type = "send_message"
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
    await callback.message.edit_reply_markup(reply_markup=None)

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
