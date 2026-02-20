from src.core.logging_config import setup_logging

logger = setup_logging(__name__, service="payments")

from src.safe_bot import SafeBot
from src.core.config import settings

#TODO сделать отправку ссылки на курс
class TelegramNotifier:

    @staticmethod
    async def notify_user_succeeded_payment(bot: SafeBot, user_id: int, amount: float):
        """
        Отправляет пользователю сообщение о платеже.
        """
        try:
            await bot.send_message(
                chat_id=int(user_id),
                text=(
                    f"""✅ **Оплата получена!**
                        Сумма: {amount} ₽
                        Доступ к курсу открыт: {settings.course_bot_link}
                        Приятного обучения! 🎓"""
                ),
                parse_mode="Markdown"
            )
            logger.info(f"📨 Sent payment confirmation to user {user_id}")

        except Exception as e:
            logger.error(f"❌ Failed to send message to user {user_id}: {e}")
            raise Exception(e)