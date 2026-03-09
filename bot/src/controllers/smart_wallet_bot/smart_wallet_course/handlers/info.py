from datetime import datetime, timezone

from aiogram import F

from src.controllers.smart_wallet_bot.smart_wallet_course.handlers.start import check_user_access_course
from src.controllers.smart_wallet_bot.smart_wallet_course.messages import messages
from src.core.logging_config import setup_logging
from src.models.sent_message import SentMessageTagEnum, SentMessageDeleteTimings
from src.views.sent_message import track_message

logger = setup_logging(__name__, service="course_bot")

from aiogram.types import CallbackQuery

from src.controllers.user_states import SmartWalletCourseStates
from src.controllers.smart_wallet_bot.smart_wallet_course.handlers import smart_wallet_router



@smart_wallet_router.callback_query(F.data == "course_info")
async def handle_info(callback: CallbackQuery):

    await callback.answer()

    user_id = callback.from_user.id

    is_access = await check_user_access_course(user_id)

    if not is_access:

        await callback.message.answer(
            "❌ <b>Нет доступа к курсу</b>\n\n",
            parse_mode="HTML"
        )

        return


    text = messages["info"]

    sent_message = await callback.message.answer(
        text=text,
    )

    await track_message(
        user_id=user_id,
        telegram_message_id=sent_message.message_id,
        tag=SentMessageTagEnum.SM_COURSE,
        stage=SmartWalletCourseStates.FINAL,
        delete_at=datetime.now(timezone.utc) + SentMessageDeleteTimings.get_extra_long(),
        delete_on_stage=SmartWalletCourseStates.EXPIRED,
    )