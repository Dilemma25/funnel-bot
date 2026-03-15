from datetime import datetime
from datetime import timezone

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F
from tortoise.transactions import in_transaction

import src.controllers.funnel_bot.day_b.messages as messages
from src.controllers.funnel_bot.day_b.file_codes import FileCodesDayB
from src.controllers.user_states import DayBStates
from src.controllers.user_states import DayCStates
from src.core.config import settings
from src.keyboards.day_b_keyborads import keyboard_b2
from src.models.offer import OfferCodesEnum
from src.models.sent_message import SentMessageTagEnum, SentMessageDeleteTimings
from src.models.user_history import EventTypeEnum
from src.views.media import get_media_by_file_code
from src.views.sent_message import track_message
from src.views.user_history import create_user_history
from src.views.user_state.update_user_state import update_user_state

from . import day_b_router


@day_b_router.callback_query(F.data == "day_b:b2:full_package")
async def social_handler(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_reply_markup(reply_markup=None)

    messages_ids = []

    message = await callback.message.answer(
        text=messages.message_B2,
        protect_content=True,
        parse_mode="Markdown",
    )

    messages_ids.append(message.message_id)

    for idx, file_code in enumerate(FileCodesDayB.REVIEWS, start=1):
        file_id = await get_media_by_file_code(
            file_code,
            OfferCodesEnum.SMART_WALLET,
        )

        reply_markup = keyboard_b2 if idx == len(FileCodesDayB.REVIEWS) else None

        message = await callback.message.answer_photo(
            photo=file_id,
            protect_content=True,
            reply_markup=reply_markup,
        )

        messages_ids.append(message.message_id)

    user_id = callback.from_user.id

    async with in_transaction() as conn:

        now = datetime.now(timezone.utc)

        #
        # await create_user_history(
        #     user_id=user_id,
        #     event_type=EventTypeEnum.STAGE_ENTERED,
        #     user_stage=DayBStates.B_2_SOCIAL_PROOF,
        #     connection=conn
        # )

        for message_id in messages_ids:
            await track_message(
                user_id=user_id,
                telegram_message_id=message_id,
                tag=SentMessageTagEnum.FUNNEL,
                stage=DayBStates.B_2_SOCIAL_PROOF,
                delete_at=now + SentMessageDeleteTimings.get_default(),
                delete_on_stage=DayCStates.C_1_PERSONAL_UPGRADE,
                connection=conn
            )

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            last_activity_at=now,
            state=DayBStates.B_2_SOCIAL_PROOF,
            connection=conn,
        )
