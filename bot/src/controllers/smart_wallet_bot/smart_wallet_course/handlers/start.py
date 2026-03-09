from datetime import datetime, timezone

from tortoise.transactions import in_transaction

from src.controllers.smart_wallet_bot.smart_wallet_course.messages import messages
from src.core.logging_config import setup_logging
from src.models.sent_message import SentMessageTagEnum, SentMessageDeleteTimings
from src.views.sent_message import track_message
from src.views.user_state.get_user_state import get_user_state

logger = setup_logging(__name__, service="course_bot")

from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from src.controllers.user_states import SmartWalletCourseStates
from src.models.offer import OfferCodesEnum
from src.views.user_state.update_user_state import update_user_state
from src.models import User
from src.models.payment import PaymentStatusEnum
from src.views.user_offer_payment import get_payment_with_status
from src.controllers.smart_wallet_bot.smart_wallet_course.handlers import smart_wallet_router


async def check_user_access_course(user_id: int):
    user = await User.get_or_none(telegram_id=user_id)

    if not user:
        logger.info(f"👤 New user {user_id} - no access")
        return False

    payment = await get_payment_with_status(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        payment_status=PaymentStatusEnum.SUCCESSFUL,
    )

    if not payment:
        logger.info(f"💳 User {user_id} - no successful payment")
        return False

    user_state = await get_user_state(
        user_id=user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
    )

    if user_state.state == SmartWalletCourseStates.EXPIRED:
        logger.info(f"Expired user {user_id} access to the course")
        return False

    return True

@smart_wallet_router.message(CommandStart())
async def handle_start(message: Message):
    """
    Стартовый хендлер для бота курса

    Логика:
    1. Проверяем есть ли юзер в БД
    2. Проверяем есть ли успешная оплата
    3. Если да — даём доступ к курсу
    4. Если нет — отправляем в воронку
    """


    user_id = message.from_user.id

    is_access = await check_user_access_course(user_id)

    if not is_access:

        await message.answer(
            "❌ <b>Нет доступа к курсу</b>\n\n",
            parse_mode="HTML"
        )

        return

    try:
        message_ids = []

        # ✅ Доступ есть — показываем курс
        logger.info(f"✅ User {user_id} has access - showing course")

        text = messages["introductory"]

        sent_message = await message.answer(
            text=text,
        )

        message_ids.append(sent_message.message_id)

        text = messages["info"]

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="▸ Смотреть 1 урок",
                callback_data="lesson_01"
            )]
        ])

        sent_message = await message.answer(
            text=text,
            reply_markup=keyboard
        )

        message_ids.append(sent_message.message_id)

        await update_user_state(
            user_id=user_id,
            offer_code=OfferCodesEnum.SMART_WALLET,
            state=SmartWalletCourseStates.STARTING
        )

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


    except Exception as e:
        logger.error(f"❌ Error in start handler for user {user_id}: {e}", exc_info=True)
        await message.answer(
            "⚠️ Произошла ошибка. Попробуйте позже или обратитесь в поддержку.",
        )