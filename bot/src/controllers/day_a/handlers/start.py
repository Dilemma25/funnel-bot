from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery
from tortoise.transactions import in_transaction

from src.keyboards.day_a_keyboards import keyboard_A1
from src.processing.task_types import TaskTypeEnum
from src.views.user import get_or_create_user
from src.views.media import get_media_by_file_code
from src.views.user_offer import get_user_offer
from src.views.user_offer import create_user_offer
from src.views.tasks import create_task
from src.models.offer import OfferCodesEnum
import src.controllers.day_a.messages as messages
from src.core.config import settings
from src.views.user_state.create_user_state import create_user_state
from src.views.user_state.update_user_state import update_user_state
from . import day_a_router
from src.controllers.day_a.timings import Timings

from datetime import datetime

from src.controllers.day_a.file_codes import FileCodes
from src.controllers.day_a.user_states import DayAStates

from src.controllers.schemas.task_payloads import DocumentTaskPayload
from src.controllers.schemas.task_payloads import MessageTaskPayload

from src.controllers.schemas.keyboard import button
from src.controllers.schemas.keyboard import keyboard


@day_a_router.message(CommandStart())
async def start_day_a(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await get_or_create_user(user_id)


    user_offer = await get_user_offer(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET
    )


    if user_offer and not settings.is_dev:

        await message.answer(
            text="Вы уже взаимодействовали с этим предложением",
            parse_mode="Markdown",
            protect_content=True,
        )

        return

    if not user_offer:

        async with in_transaction() as conn:

            user_offer = await create_user_offer(
                user_id=user_id,
                offer_code=OfferCodesEnum.SMART_WALLET,
                connection=conn,
            )

            await create_user_state(
                user_id=user_id,
                offer_id=user_offer.offer_id,
                connection=conn,
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

    user_id = message.from_user.id

    await update_user_state(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        last_activity_at=datetime.now(settings.timezone),
        state=DayAStates.A_1_STARTED
    )


@day_a_router.callback_query(F.data == "day_a:a1:start")
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

        task_a3_file_id = await get_media_by_file_code(FileCodes.CHECK_LIST, OfferCodesEnum.SMART_WALLET)

        task_a3_type = TaskTypeEnum.SEND_DOCUMENT
        task_a3_payload = DocumentTaskPayload(
            user_id=user_id,
            text=messages.message_A3,
            file_id=task_a3_file_id,
        )

        task_a3_time_run = datetime.now(settings.timezone) + Timings.CHECKLIST_DELAY

        await create_task(user_id, task_a3_type, task_a3_payload.model_dump_json(), task_a3_time_run, conn)

        #Таска на клавиатуру после чек листа

        task_a3_kb_type = TaskTypeEnum.SEND_MESSAGE

        task_a3_kb_payload = MessageTaskPayload(
            user_id=user_id,
            text=messages.message_A3_kb,
            keyboard=keyboard(
                [
                    button(text="Нашёл(ла) несколько пунктов про себя", callback_data="day_a:a3:found"),
                ],
                [
                    button(text="Пока не вижу явных проблем", callback_data="day_a:a3:not_found")
                ]
            ),
        )

        task_a3_kb_time_run = datetime.now(settings.timezone) + Timings.CHECKLIST_KEYBOARD_DELAY

        await create_task(user_id, task_a3_kb_type, task_a3_kb_payload.model_dump_json(), task_a3_kb_time_run, conn)

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            last_activity_at=datetime.now(settings.timezone),
            state=DayAStates.A_2_VIDEO_LID_SENT,
            connection=conn,
        )

