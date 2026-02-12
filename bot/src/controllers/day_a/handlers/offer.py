from datetime import datetime
import logging

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from tortoise.transactions import in_transaction

from src.controllers.day_a.file_codes import FileCodes
from src.models.offer import OfferCodesEnum
from src.controllers.day_a import messages
from src.controllers.day_a.handlers import day_a_router
from src.controllers.day_a.timings import Timings
from src.core.config import config
from src.keyboards.day_a_keyboards import keyboard_A9_2_2
from src.states.day_a import DayAStates
from src.views.media import get_media_by_file_code
from src.views.tasks import create_task


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#TODO сделать парсинг цены из базы
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

            now = datetime.now(config["TIMEZONE"])
            offer_code = OfferCodesEnum.SMART_WALLET

            # ===== ТАСКА 1: Установка скидки + оффер =====
            payload_offer = {
                "user_id": user_id,
                "text": messages.message_A9,
                "keyboard": [
                    [{"text": "Забрать за 2 490 ₽", "callback_data": "day_a:a9:buy"}],
                    [{"text": "Узнать подробнее", "callback_data": "day_a:a9:faq"}],
                ],
                # Параметры скидки
                "offer_code": offer_code,
                #TODO поменить прайсы скидок в отдельном файле с констами
                "discount_price": 2490,
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
                    [{"text": "💳 Оплатить 2 490 ₽", "callback_data": "day_a:a9:buy"}],
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

        # Если транзакция успешна
        await state.set_state(DayAStates.a_8_video_note_method_sent)

    except Exception as e:
        logger.error(f"❌ Ошибка создания тасок: {e}", exc_info=True)
        # await callback.message.answer("Произошла ошибка. Попробуй позже.")


@day_a_router.callback_query(
    # StateFilter(DayAStates.a_9_offer_sent),
    StateFilter(DayAStates.a_8_video_note_method_sent),
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
            [{"text": "✅ Забрать за 2 490 ₽", "callback_data": "day_a:a9_2_1:buy"}],
            [{"text": "👁 Посмотреть отзывы", "callback_data": "day_a:a9_2_2:reviews"}],
        ]

        payload = {
            "user_id": user_id,
            "text": messages.message_A9_2_1,
            "keyboard": keyboard_json
        }

        task_type = "send_message"
        time_run = datetime.now(config["TIMEZONE"]) + Timings.RETURN_TO_OFFER

        await create_task(user_id, task_type, payload, time_run, conn)

    await state.set_state(DayAStates.a_9_2_faq_sent)

@day_a_router.callback_query(
    StateFilter(DayAStates.a_9_2_faq_sent),
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

    await state.set_state(DayAStates.day_a_reviews_sent)
