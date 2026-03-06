from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.core.logging_config import setup_logging
from src.core.config import settings
from src.states.support import SupportStates
from src.safe_bot import SafeBot

from . import support_router

logger = setup_logging(__name__, service="bot")


@support_router.message(Command("help"))
async def handle_help(message: Message, state: FSMContext):
    """Команда /help - начало обращения в поддержку"""

    await message.answer(
        "📞 **Обращение в поддержку**\n\n"
        "Опишите вашу проблему одним сообщением.\n\n"
        "Например:\n"
        "• Оплатил, но не получил доступ к курсу\n"
        "Напишите ваше сообщение:",
        parse_mode="Markdown"
    )

    await state.set_state(SupportStates.waiting_for_message)


@support_router.message(SupportStates.waiting_for_message, F.text)
async def receive_support_message(message: Message, state: FSMContext):
    """Получаем сообщение от юзера и пересылаем админам"""

    user_id = message.from_user.id
    username = message.from_user.username or "нет username"
    full_name = message.from_user.full_name or "Unknown"
    user_message = message.text

    # Формируем сообщение для админов
    admin_notification = (
        f"🆘 **ОБРАЩЕНИЕ В ПОДДЕРЖКУ**\n\n"
        f"👤 От: {full_name}\n"
        f"🆔 User ID: `{user_id}`\n"
        f"📱 Username: @{username}\n\n"
        f"💬 **Сообщение:**\n{user_message}"
    )

    bot = SafeBot(settings.funnel_bot_token)

    admin_id = settings.admin_ids[0]

    try:
        await bot.send_message(
            chat_id=settings.admin_ids[0],
            text=admin_notification,
            parse_mode="Markdown"
        )
        logger.info(f"📨 Support message sent to admin {admin_id}")

    except Exception as e:
        logger.error(f"❌ Failed to send to admin {admin_id}: {e}")

    await bot.session.close()

    await message.answer(
        "✅ **Ваше обращение отправлено!**\n\n"
        "Мы свяжемся с вами в ближайшее время.\n",
        parse_mode="Markdown"
    )

    await state.clear()


@support_router.message(Command("cancel"))
async def handle_cancel(message: Message, state: FSMContext):
    """Отмена обращения"""

    await state.clear()
    await message.answer("❌ Обращение отменено.")