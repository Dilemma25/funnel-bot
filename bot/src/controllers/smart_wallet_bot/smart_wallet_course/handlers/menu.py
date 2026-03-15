from datetime import timezone, datetime

from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from src.controllers.smart_wallet_bot.smart_wallet_course.handlers import smart_wallet_router
from src.controllers.user_states import SmartWalletCourseStates
from src.models.offer import OfferCodesEnum
from src.models.sent_message import SentMessageTagEnum, SentMessageDeleteTimings
from src.views.sent_message import track_message
from src.views.user_state.get_user_state import get_user_state
from src.controllers.smart_wallet_bot.smart_wallet_course.handlers.start import check_user_access_course


def lesson_state_to_callback_data(state: SmartWalletCourseStates | str):
    _, lesson, number = state.split(":")
    return f"{lesson}_{number}"

def lesson_button_text(state: SmartWalletCourseStates, number: int) -> str:
    if state == SmartWalletCourseStates.LESSON_OPENING:
        return "▸ Вступительный урок"
    return f"▸ Урок {number}"

def build_lessons_keyboard(end_state: SmartWalletCourseStates):
    end = end_state

    buttons = [[
        InlineKeyboardButton(
            text="▸ Как проходит курс?",
            callback_data="course_info"
        )
    ]]

    # Если пользователь только начал курс, показываем первый урок
    if end == SmartWalletCourseStates.STARTING or end.order < SmartWalletCourseStates.STARTING.order:
        first_lesson = SmartWalletCourseStates.LESSON_1
        buttons.append([
            InlineKeyboardButton(
                text="▸ Урок 1",
                callback_data=lesson_state_to_callback_data(first_lesson)
            )
        ])
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    # Для всех остальных состояний — обычная логика
    lesson_number = 1
    for state in SmartWalletCourseStates:

        if state in (
                SmartWalletCourseStates.STARTING,
                SmartWalletCourseStates.FINAL,
        ):
            continue

        if not (SmartWalletCourseStates.LESSON_1.order <= state.order <= end.order):
            continue

        text = lesson_button_text(state, lesson_number)

        if state != SmartWalletCourseStates.LESSON_OPENING:
            lesson_number += 1

        buttons.append([
            InlineKeyboardButton(
                text=text,
                callback_data=lesson_state_to_callback_data(state)
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

@smart_wallet_router.message(Command("menu"))
async def menu(message: Message):

    user_id = message.from_user.id

    is_access = await check_user_access_course(user_id)

    if not is_access:
        await message.answer(
            "❌ <b>Доступ к курсу не найден</b>\n\n",
            parse_mode="HTML"
        )

        return

    user_state = await get_user_state(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET
    )

    end = SmartWalletCourseStates(user_state.state)

    keyboard = build_lessons_keyboard(end)

    message = await message.answer(
        text="Выберите урок",
        reply_markup=keyboard
    )

    await track_message(
        user_id=user_id,
        telegram_message_id=message.message_id,
        tag=SentMessageTagEnum.SM_COURSE,
        stage=user_state.state,
        delete_at=datetime.now(timezone.utc) + SentMessageDeleteTimings.get_extra_long(),
        delete_on_stage=SmartWalletCourseStates.EXPIRED,
    )
