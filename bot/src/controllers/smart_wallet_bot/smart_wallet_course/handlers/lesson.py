import asyncio
from datetime import timezone
from datetime import datetime

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from tortoise.transactions import in_transaction

from src.controllers.smart_wallet_bot.smart_wallet_course.handlers import smart_wallet_router
from src.controllers.smart_wallet_bot.smart_wallet_course.handlers.menu import lesson_state_to_callback_data
from src.controllers.smart_wallet_bot.smart_wallet_course.handlers.start import check_user_access_course
from src.controllers.smart_wallet_bot.smart_wallet_course.messages import messages
from src.controllers.user_states import get_state_by_callback
from src.controllers.user_states import get_state_order
from src.controllers.user_states import SmartWalletCourseStates
from src.models.media import MediaFileTypeEnum
from src.models.offer import OfferCodesEnum
from src.models.sent_message import SentMessageTagEnum
from src.models.sent_message import SentMessageDeleteTimings
from src.views.media.get_media_by_prefix import get_media_by_prefix
from src.views.sent_message import track_message
from src.views.user_state.get_user_state import get_user_state


def get_next_lesson_callback(callback_data: str) -> str:
    """Возвращает callback следующего урока или 'course_final'"""

    current_state = get_state_by_callback(callback_data=callback_data)

    if not isinstance(current_state, SmartWalletCourseStates):
        return "course_final"

    lessons_values = [s for s in SmartWalletCourseStates
                      if s not in (SmartWalletCourseStates.STARTING, SmartWalletCourseStates.FINAL,
                                   SmartWalletCourseStates.EXPIRED)]

    try:
        index = lessons_values.index(current_state.value)
    except ValueError:
        return "course_final"

    # Следующий урок или финальный итог
    if index + 1 < len(lessons_values):
        next_state = lessons_values[index + 1]
        return lesson_state_to_callback_data(next_state)
    else:
        return "course_final"

def build_next_lesson_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    next_callback = get_next_lesson_callback(callback_data)

    if next_callback == "course_final":
        text = "📊 Итоги курса"
    else:
        text = f"▸ Следующий урок"

    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text=text,
            callback_data=next_callback
        )
    ]])

@smart_wallet_router.callback_query(F.data.startswith("lesson_"))
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

    current_lesson_state = get_state_by_callback(callback_data=callback_data)

    current_user_state_object = await get_user_state(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET
    )

    if not current_user_state_object:
        await callback.message.answer("❌ Произошла ошибка. Мы уже работаем над её исправлением.")
        return

    current_user_state = current_user_state_object.state

    current_user_state_order = get_state_order(current_user_state)

    #Если сейчас юзер находится на новом для себя уроке, мы сохраняем его состояние
    if current_lesson_state.order > current_user_state_order:
        current_user_state_object.state = current_lesson_state
        await current_user_state_object.save()

    media_files = await get_media_by_prefix(
        prefix=callback_data,
        offer_code=OfferCodesEnum.SMART_WALLET
    )

    message_ids = []

    message = messages[callback_data]

    video_files = []

    for media_file in media_files:
        if media_file.file_type == MediaFileTypeEnum.VIDEO:
            video_files.append(media_file)

    for video_file in video_files:

        caption = None

        part = video_file.code.split("_")[-1]

        if part.isdigit():
            caption = f"Часть {part}"

        message_video = await callback.message.answer_video(
            video=video_file.file_id,
            caption=caption
        )

        message_ids.append(message_video.message_id)

        await asyncio.sleep(0.25)

    keyboard = build_next_lesson_keyboard(callback_data)

    for media_file in media_files:
        if media_file.file_type != MediaFileTypeEnum.VIDEO:

            file = media_file.file_id

            message_document = await callback.message.answer_document(
                document=file,
            )

            message_ids.append(message_document.message_id)

            await asyncio.sleep(0.25)

    message_text = await callback.message.answer(
        text=message,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )

    message_ids.append(message_text.message_id)

    await asyncio.sleep(0.25)

    async with in_transaction() as conn:

        for message_id in message_ids:

            await track_message(
                user_id=user_id,
                telegram_message_id=message_id,
                tag=SentMessageTagEnum.SM_COURSE,
                stage=current_lesson_state,
                delete_at=datetime.now(timezone.utc) + SentMessageDeleteTimings.get_extra_long(),
                delete_on_stage=SmartWalletCourseStates.EXPIRED,
                connection=conn
            )

