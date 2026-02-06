from datetime import datetime

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from tortoise.transactions import in_transaction

from src.models.offer import OfferCodesEnum
from src.controllers.day_a import messages
from src.controllers.day_a.handlers import day_a_router
from src.controllers.day_a.timings import Timings
from src.core.config import config
from src.keyboards.day_a_keyboards import keyboard_A9_2_2
from src.states.day_a import DayAStates
from src.views.media import get_media_by_file_code
from src.views.tasks import create_task
from src.views.user_offer import set_discount


@day_a_router.callback_query(F.data == "day_a:a7:next")
async def handle_a7_next(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_reply_markup(reply_markup=None)

    offer_id = await state.get_value("offer_id")

    file_id = await get_media_by_file_code("V2_krujok_metod", offer_id)

    await callback.message.answer_video_note(
        video_note=file_id,
        protect_content=True,
    )

    async with in_transaction() as conn:
        user_id = callback.from_user.id
        offer_code = OfferCodesEnum.SMART_WALLET

        await set_discount(
            user_id=user_id,
            offer_code=offer_code,
            discount_price=2.490,
            discount_duration=Timings.DISCOUNT_TIMER,
            connection=conn
        )

        #Таска на оффер
        keyboard_json = [
            [{"text": "Забрать за 2 490 ₽", "callback_data": "day_a:a9:buy"}],
            [{"text": "Узнать подробнее", "callback_data": "day_a:a9:faq"}],
        ]

        user_id = callback.from_user.id

        payload = {
            "user_id": user_id,
            "text": messages.message_A9,
            "keyboard": keyboard_json
        }

        task_type = "send_message_with_keyboard"
        time_run = datetime.now(config["TIMEZONE"]) + Timings.OFFER_DELAY

        await create_task(user_id, task_type, payload, time_run, conn)

        #Таска на напоминание о таймере
        keyboard_json = [
            [{"text": "💳 Оплатить 2 490 ₽", "callback_data": "day_a:a9:buy"}],
        ]

        payload = {
            "user_id": user_id,
            "text": messages.message_A9_1_1,
            "keyboard": keyboard_json
        }

        task_type = "send_message_with_keyboard"
        time_run = datetime.now(config["TIMEZONE"]) + Timings.REMEMBER_ABOUT_DISCOUNT

        await create_task(user_id, task_type, payload, time_run, conn)

        #Главный таймер на скидку, после него конец первого дня
        payload = {
            "user_id": user_id,
            "text": messages.message_A10_FINAL,
        }

        task_type = "send_message"
        time_run = datetime.now(config["TIMEZONE"]) + Timings.DISCOUNT_TIMER

        await create_task(user_id, task_type, payload, time_run, conn)

    await state.set_state(DayAStates.a_8_video_note_method_sent)

@day_a_router.callback_query(
    StateFilter(DayAStates.a_9_offer_sent),
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

        task_type = "send_message_with_keyboard"
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

    offer_id = await state.get_value("offer_id")

    for i in range(1, 6):

        file_id = await get_media_by_file_code(f"otzyv_{i}", offer_id)

        reply_markup = None

        if i == 5:
            reply_markup = keyboard_A9_2_2

        await callback.message.answer_photo(
            photo=file_id,
            protect_content=True,
            reply_markup=reply_markup,
        )

    await state.set_state(DayAStates.day_a_reviews_sent)
