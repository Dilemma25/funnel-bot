from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message

from src.controllers.funnel_bot.admin.handlers import admin_router
from src.core.config import settings
from src.safe_bot import SafeBot


@admin_router.message(Command("reply"), F.from_user.id.in_(settings.admin_ids))
async def admin_reply(message: Message):
    """
    Формат: /reply <user_id> <текст>
    Пример: /reply 1440024192 Проблема решена!
    """

    args = message.text.split(maxsplit=2)

    if len(args) < 3:
        await message.answer("❌ Формат: /reply <user_id> <текст>")
        return

    try:
        user_id = int(args[1])
        reply_text = args[2]
    except:
        await message.answer("❌ Неверный user_id")
        return

    bot = SafeBot(settings.funnel_bot_token)

    try:
        await bot.send_message(
            chat_id=user_id,
            text=f"💬 **Ответ от поддержки:**\n\n{reply_text}",
            parse_mode="Markdown"
        )
        await message.answer(f"✅ Отправлено пользователю {user_id}")

    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

    finally:
        await bot.session.close()