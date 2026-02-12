from aiogram import F
from aiogram.filters import CommandStart
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery
from tortoise.transactions import in_transaction

from src.keyboards.day_a_keyboards import keyboard_A1
from src.views.user import get_or_create_user
from src.views.media import get_media_by_file_code
from src.views.user_offer import get_user_offer
from src.views.user_offer import create_user_offer
from src.views.tasks import create_task
from src.states.day_a import DayAStates
from src.models.offer import OfferCodesEnum
import src.controllers.day_a.messages as messages
from src.core.config import config
from . import day_a_router
from src.controllers.day_a.timings import Timings

from datetime import datetime

from ..file_codes import FileCodes


@day_a_router.message(CommandStart())
async def start_day_a(message: Message, state: FSMContext):
    await get_or_create_user(message.from_user.id)

    user_offer = await get_user_offer(
        user_id=message.from_user.id,
        offer_code=OfferCodesEnum.SMART_WALLET
    )


    if user_offer and not config["DEV_MODE"]:

        await message.answer(
            text="Вы уже взаимодействовали с этим предложением",
            parse_mode="Markdown",
            protect_content=True,
        )

        return

    if not user_offer:

        user_id = message.from_user.id

        await create_user_offer(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET
        )

    await state.update_data(
        offer_code=OfferCodesEnum.SMART_WALLET,
    )

    await message.answer(
        messages.message_A1,
        parse_mode="Markdown",
        reply_markup=keyboard_A1,
        protect_content=True,
    )

    await state.set_state(DayAStates.a_1_greeting_sent)

    # #TODO Удалить
    #
    user_id = message.from_user.id

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
            # TODO поменить прайсы скидок в отдельном файле с констами
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



@day_a_router.callback_query(
    StateFilter(DayAStates.a_1_greeting_sent),
    F.data == "day_a:a1:start"
)
async def send_video_lid(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    user_id = callback.from_user.id

    await callback.message.edit_reply_markup(reply_markup=None)

    file_id = await get_media_by_file_code(
        file_code=FileCodes.LID_MAGNET,
        offer_code=OfferCodesEnum.SMART_WALLET,
    )

    await callback.message.answer_video(
        video=file_id,
        caption=messages.message_A2,
        protect_content=True,
        parse_mode="Markdown",
    )

    async with in_transaction() as conn:
        #Таска A3
        task_a3_type = "send_document"
        task_a3_file_id = await get_media_by_file_code(FileCodes.CHECK_LIST, OfferCodesEnum.SMART_WALLET)

        task_a3_payload = {
            "user_id": user_id,
            "text": messages.message_A3,
            "file_id": task_a3_file_id
        }

        task_a3_time_run = datetime.now(config["TIMEZONE"]) + Timings.CHECKLIST_DELAY

        await create_task(user_id, task_a3_type, task_a3_payload, task_a3_time_run, conn)

        #Таска на клавиатуру после чек листа
        task_a3_kb_type = "send_message"

        task_a3_kb_keyboard_json = [
            [{"text": "Нашёл(ла) несколько пунктов про себя", "callback_data": "day_a:a3:found"}],
            [{"text": "Пока не вижу явных проблем", "callback_data": "day_a:a3:not_found"}],
        ]

        task_a3_kb_payload = {
            "user_id": user_id,
            "text": messages.message_A3_kb,
            "keyboard": task_a3_kb_keyboard_json
        }

        task_a3_kb_time_run = datetime.now(config["TIMEZONE"]) + Timings.CHECKLIST_KEYBOARD_DELAY

        await create_task(user_id, task_a3_kb_type, task_a3_kb_payload, task_a3_kb_time_run, conn)

    await state.set_state(DayAStates.a_2_video_sent)
