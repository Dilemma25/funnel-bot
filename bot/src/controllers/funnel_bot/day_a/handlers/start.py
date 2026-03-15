from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery
from tortoise.transactions import in_transaction

from src.keyboards.day_a_keyboards import keyboard_A1
from src.models.sent_message import SentMessageTagEnum
from src.models.sent_message import SentMessageDeleteTimings
from src.models.user_history import EventTypeEnum
from src.processing.task_types import TaskTypeEnum
from src.views.sent_message import track_message
from src.views.user import get_or_create_user
from src.views.media import get_media_by_file_code
from src.views.user_history import create_user_history
from src.views.user_offer import get_user_offer
from src.views.user_offer import create_user_offer
from src.views.tasks import create_task
from src.models.offer import OfferCodesEnum
import src.controllers.funnel_bot.day_a.messages as messages_day_a
import src.controllers.funnel_bot.day_b.messages as messages_day_b
import src.controllers.funnel_bot.day_c.messages as messages_day_c
from src.core.config import settings
from src.views.user_state.create_user_state import create_user_state
from src.views.user_state.update_user_state import update_user_state
from . import day_a_router
from src.controllers.funnel_bot.day_a.timings import Timings
from src.controllers.funnel_bot.day_a.file_codes import FileCodes
from src.controllers.user_states import DayAStates
from src.controllers.user_states import DayBStates
from src.controllers.user_states import DayCStates

from src.controllers.schemas.task_payloads import DocumentTaskPayload, FinishFunnelTaskPayload
from src.controllers.schemas.task_payloads import MessageTaskPayload

from src.controllers.schemas.keyboard import button
from src.controllers.schemas.keyboard import keyboard

from datetime import datetime, timezone


@day_a_router.message(CommandStart())
async def start_day_a(message: Message, state: FSMContext):
    user_id = message.from_user.id

    await get_or_create_user(user_id)


    user_offer = await get_user_offer(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET
    )

    if settings.is_dev:
        await message.answer(
            text="Бот запущен в режиме разработки"
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

    message = await message.answer(
        messages_day_a.message_A1,
        parse_mode="Markdown",
        reply_markup=keyboard_A1,
        protect_content=True,
    )

    async with in_transaction() as conn:

        now = datetime.now(timezone.utc)

        # await create_user_history(
        #     user_id=user_id,
        #     event_type=EventTypeEnum.STAGE_ENTERED,
        #     user_stage=DayAStates.A_1_STARTED,
        #     connection=conn
        # )

        await track_message(
            user_id=user_id,
            telegram_message_id=message.message_id,
            tag=SentMessageTagEnum.FUNNEL,
            stage=DayAStates.A_1_STARTED,
            delete_on_stage=DayBStates.B_1_COLD_SHOWER,
            delete_at=now + SentMessageDeleteTimings.get_long(),
            connection=conn
        )

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            last_activity_at=datetime.now(settings.timezone),
            state=DayAStates.A_1_STARTED,
            connection=conn
        )

        # Создание тасок на
        # Начало DAY_B
        # Начало DAY_C
        # Конец воронки

        # ===== ТАСКА 1: Начало день B =====
        run_at = now + Timings.DAY_B_START

        payload = MessageTaskPayload(
            user_id=user_id,
            text=messages_day_b.message_B2,
            keyboard=keyboard(
                [
                    button(text="Какой полный пакет?", callback_data="day_b:b2:full_package"),
                ],
            ),
            message_stage=DayBStates.B_1_COLD_SHOWER,
            message_tag=SentMessageTagEnum.FUNNEL,
            delete_on_stage=DayCStates.C_1_PERSONAL_UPGRADE,
            delete_at=run_at + SentMessageDeleteTimings.get_long(),
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.SEND_MESSAGE,
            payload=payload.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

        # ===== ТАСКА 2: Начало день С =====

        run_at = now + Timings.DAY_C_START

        payload = MessageTaskPayload(
            user_id=user_id,
            text=messages_day_c.message_c1,
            keyboard=keyboard(
                [
                    button(text="Хочу апгрейд", callback_data="day_c:c2:offer"),
                ],
            ),
            message_stage=DayCStates.C_1_PERSONAL_UPGRADE,
            message_tag=SentMessageTagEnum.FUNNEL,
            delete_on_stage=DayCStates.FINAL,
            delete_at=run_at + SentMessageDeleteTimings.get_long(),
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.SEND_MESSAGE,
            payload=payload.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

        # ===== ТАСКА 3: Финал воронки =====

        run_at = now + Timings.FUNNEL_FINAL

        payload = FinishFunnelTaskPayload(
            user_id=user_id,
            text=messages_day_c.message_c3,
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


@day_a_router.callback_query(F.data == "day_a:a1:start")
async def send_video_lid(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    user_id = callback.from_user.id

    await callback.message.edit_reply_markup(reply_markup=None)

    file_id = await get_media_by_file_code(
        file_code=FileCodes.LID_MAGNET,
        offer_code=OfferCodesEnum.SMART_WALLET,
    )

    message = await callback.message.answer_video(
        video=file_id,
        caption=messages_day_a.message_A2,
        protect_content=True,
        parse_mode="Markdown",
    )

    async with in_transaction() as conn:

        now = datetime.now(timezone.utc)

        # await create_user_history(
        #     user_id=user_id,
        #     event_type=EventTypeEnum.STAGE_ENTERED,
        #     user_stage=DayAStates.A_2_VIDEO_LID_SENT,
        #     connection=conn
        # )

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            last_activity_at=now,
            state=DayAStates.A_2_VIDEO_LID_SENT,
            connection=conn,
        )

        await track_message(
            user_id=user_id,
            stage=DayAStates.A_2_VIDEO_LID_SENT,
            telegram_message_id=message.message_id,
            tag=SentMessageTagEnum.FUNNEL,
            delete_on_stage=DayBStates.B_1_COLD_SHOWER,
            delete_at=now + SentMessageDeleteTimings.get_long(),
            connection=conn,
        )

        # ===== ТАСКА 1: Чек лист (A3) =====
        run_at = now + Timings.CHECKLIST_DELAY
        task_a3_file_id = await get_media_by_file_code(FileCodes.CHECK_LIST, OfferCodesEnum.SMART_WALLET)

        task_a3_payload = DocumentTaskPayload(
            user_id=user_id,
            text=messages_day_a.message_A3,
            file_id=task_a3_file_id,
            message_stage=DayAStates.A_3_CHECKLIST_SENT,
            message_tag=SentMessageTagEnum.FUNNEL,
            delete_at=run_at + SentMessageDeleteTimings.get_short(),
            delete_on_stage=DayAStates.FINAL
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.SEND_DOCUMENT,
            payload=task_a3_payload.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

        # ===== ТАСКА 2: Клавиатура после чек листа =====
        run_at = now + Timings.CHECKLIST_KEYBOARD_DELAY

        payload = MessageTaskPayload(
            user_id=user_id,
            text=messages_day_a.message_A3_kb,
            keyboard=keyboard(
                [
                    button(text="Нашёл(ла) несколько пунктов про себя", callback_data="day_a:a3:found"),
                ],
                [
                    button(text="Пока не вижу явных проблем", callback_data="day_a:a3:not_found")
                ]
            ),
            message_stage=DayAStates.A_3_CHECKLIST_SENT,
            message_tag=SentMessageTagEnum.FUNNEL,
            delete_on_stage=DayBStates.B_1_COLD_SHOWER,
            delete_at=run_at + SentMessageDeleteTimings.get_long(),
        )

        await create_task(
            user_id=user_id,
            task_type=TaskTypeEnum.SEND_MESSAGE,
            payload=payload.model_dump_json(),
            run_at=run_at,
            connection=conn
        )

