from datetime import datetime

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from src.controllers.day_a import messages
from src.controllers.day_a.handlers import day_a_router
from src.controllers.day_a.timings import Timings
from src.core.config import config
from src.keyboards.day_a_keyboards import keyboard_A9_2_2
from src.states.day_a import DayAStates
from src.views.media import get_by_file_name
from src.views.tasks import create


@day_a_router.callback_query(F.data == "day_a:a7:next")
async def handle_a7_next(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await callback.message.edit_reply_markup(reply_markup=None)

    file_id = await get_by_file_name("V2_krujok_metod")

    await callback.message.answer_video_note(
        video_note=file_id,
        protect_content=True,
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

    await create(user_id, task_type, payload, time_run)

    await state.set_state(DayAStates.a_9_offer_sent)

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

    await create(user_id, task_type, payload, time_run)

    #Главный таймер на скидку, после него конец первого дня
    payload = {
        "user_id": user_id,
        "text": messages.message_A10_FINAL,
    }

    task_type = "send_message"
    time_run = datetime.now(config["TIMEZONE"]) + Timings.DISCOUNT_TIMER

    await create(user_id, task_type, payload, time_run)

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

    keyboard_json = [
        [{"text": "✅ Забрать за 2 490 ₽", "callback_data": "day_a:a9_2_1:buy"}],
        [{"text": "👁 Посмотреть отзывы", "callback_data": "day_a:a9_2_2:reviews"}],
    ]

    user_id = callback.from_user.id

    payload = {
        "user_id": user_id,
        "text": messages.message_A9_2_1,
        "keyboard": keyboard_json
    }

    task_type = "send_message_with_keyboard"
    time_run = datetime.now(config["TIMEZONE"]) + Timings.RETURN_TO_OFFER

    await create(user_id, task_type, payload, time_run)

    await state.set_state(DayAStates.a_9_2_faq_sent)

@day_a_router.callback_query(
    StateFilter(DayAStates.a_9_2_faq_sent),
    F.data == "day_a:a9_2_2:reviews"
)
async def handle_reviews(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    for i in range(1, 6):
        file_id = await get_by_file_name(f"otzyv_{i}")

        reply_markup = None

        if i == 5:
            reply_markup = keyboard_A9_2_2

        await callback.message.answer_photo(
            photo=file_id,
            protect_content=True,
            reply_markup=reply_markup,
        )

    await state.set_state(DayAStates.day_a_reviews_sent)



#TODO сделать оплаты
@day_a_router.callback_query(F.data.contains(":buy"))
async def handle_buy(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer("PLACEHOLDER")

