import asyncio
from datetime import timezone
from datetime import datetime

from aiogram import F
from aiogram.types import CallbackQuery
from tortoise.transactions import in_transaction

from src.controllers.smart_wallet_bot.smart_wallet_course.handlers import smart_wallet_router
from src.controllers.smart_wallet_bot.smart_wallet_course.handlers.start import check_user_access_course
from src.controllers.smart_wallet_bot.smart_wallet_course.messages import messages
from src.controllers.user_states import SmartWalletCourseStates
from src.core.config import settings
from src.models.offer import OfferCodesEnum
from src.models.sent_message import SentMessageTagEnum
from src.models.sent_message import SentMessageDeleteTimings
from src.views.media import get_media_by_file_code
from src.views.sent_message import track_message


@smart_wallet_router.callback_query(F.data == "course_final")
async def handle_lesson(
        callback: CallbackQuery,
):
    await callback.answer()

    callback_data = callback.data

    user_id = callback.from_user.id

    is_access = await check_user_access_course(user_id)

    if not is_access:
        await callback.message.answer(
            "❌ <b>Нет доступа к курсу</b>\n\n",
            parse_mode="HTML"
        )

        return

    check_list = await get_media_by_file_code(
        file_code="course_final_checklist",
        offer_code=OfferCodesEnum.SMART_WALLET
    )

    final_message = messages[callback_data]

    final_table_link = settings.course_bot_final_table_link

    message_ids = []

    sent_message = await callback.message.answer_document(
        document=check_list
    )

    await asyncio.sleep(0.25)

    message_ids.append(sent_message.message_id)

    sent_message = await callback.message.answer(
        text=final_table_link
    )

    await asyncio.sleep(0.25)

    message_ids.append(sent_message.message_id)

    sent_message = await callback.message.answer(
        text=final_message
    )

    await asyncio.sleep(0.25)

    message_ids.append(sent_message.message_id)

    async with in_transaction() as conn:

        for message_id in message_ids:

            await track_message(
                user_id=user_id,
                telegram_message_id=message_id,
                tag=SentMessageTagEnum.SM_COURSE,
                stage=SmartWalletCourseStates.FINAL,
                delete_at=datetime.now(timezone.utc) + SentMessageDeleteTimings.get_extra_long(),
                delete_on_stage=SmartWalletCourseStates.EXPIRED,
                connection=conn
            )


