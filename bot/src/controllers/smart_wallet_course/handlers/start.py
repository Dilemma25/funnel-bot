from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from src.core.logging_config import setup_logging

logger = setup_logging(__name__, service="course_bot")

from src.models import User
from src.models.payment import PaymentStatusEnum
from src.views.user_offer_payment import get_payment_with_status

from src.controllers.smart_wallet_course.handlers import smart_wallet_router

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

    try:
        # Проверяем существование юзера
        user = await User.get_or_none(telegram_id=user_id)

        if not user:
            logger.info(f"👤 New user {user_id} - no access")
            await message.answer(
                "❌ <b>Доступ к курсу не найден</b>\n\n",
                parse_mode="HTML"
            )
            return

        # Проверяем наличие успешной оплаты
        payment = await get_payment_with_status(
            user_id=user_id,
            offer_code="SMART_WALLET",  # или settings.course_offer_code
            payment_status=PaymentStatusEnum.SUCCESSFUL,
            order_by="newest"
        )

        if not payment:
            logger.info(f"💳 User {user_id} - no successful payment")
            await message.answer(
                "❌Курс не оплачен",
                parse_mode="HTML"
            )
            return

        # ✅ Доступ есть — показываем курс
        logger.info(f"✅ User {user_id} has access - showing course")

        text = (
            "<b>Привет.</b>\n"
            "Если ты читаешь это сообщение — ты уже внутри курса.\n"
            "И это хорошее решение.\n\n"
            "Сразу договоримся:\n"
            "этот курс не про быстрые деньги и не про волшебные формулы.\n\n"
            "➤ Он про <b>контроль</b>, <b>ясность</b> и <b>систему</b>. "
            "Про понимание, куда уходят деньги и как выстроить работу с ними без постоянного напряжения."
        )

        await message.answer(
            text=text,
            parse_mode="HTML"
        )

        text = (
            "✦ <b>Как проходит курс</b>\n\n"
            "⇨ Уроки появляются последовательно;\n"
            "⇨ Каждый урок доступен 45 часов;\n"
            "⇨ Чтобы вернуться к предыдущим урокам — используй команду /menu;\n"
            "⇨ Задания важно выполнять, а не просто смотреть.\n\n"
            "Двигайся шаг за шагом.\n"
            "Без спешки."
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="▸ [Смотреть 1 урок]",
                callback_data="lesson_1"
            )]
        ])

        await message.answer(
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )

    except Exception as e:
        logger.error(f"❌ Error in start handler for user {user_id}: {e}", exc_info=True)
        await message.answer(
            "⚠️ Произошла ошибка. Попробуйте позже или обратитесь в поддержку.",
        )