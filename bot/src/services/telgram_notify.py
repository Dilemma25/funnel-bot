from src.core.logging_config import setup_logging

logger = setup_logging(__name__, service="payments")

from src.safe_bot import SafeBot
from src.core.config import settings


class TelegramNotifier:

    @staticmethod
    async def notify_user_succeeded_payment(
            bot: SafeBot,
            user_id: int,
            amount: float,
            user_email: str,
    ):
        """
        Отправляет пользователю сообщение о выполненном платеже.
        """
        try:
            await bot.send_message(
                chat_id=int(user_id),
                text=(
                    f"✅ **Оплата успешно завершена!**\n\n"
                    f"━━━━━━━━━━━━━━━━━━━━\n"
                    f"💰 **Сумма:** {amount:.0f} ₽\n"
                    f"📧 Чек отправлен на: `{user_email}`\n"
                    f"━━━━━━━━━━━━━━━━━━━━"
                ),
                parse_mode="Markdown"
            )
            logger.info(f"📨 Sent payment confirmation to user {user_id}")

        except Exception as e:
            logger.error(f"❌ Failed to send message to user {user_id}: {e}")
            raise Exception(e)

    @staticmethod
    async def notify_course_access(
            bot: SafeBot,
            user_id: int,
            course_name: str,
    ):
        """
        Отправляет пользователю уведомление о доступе к курсу

        Args:
            bot: SafeBot инстанс
            user_id: Telegram ID пользователя
            course_name: Название курса
        """
        try:

            text = (
                f"🎓 **Доступ к курсу открыт!**\n\n"
                f"📚 **Курс:** *{course_name}*\n"
                f"Переходи в бот с курсом: {settings.course_bot_link}\n\n"
                f"Приятного обучения! 🙌"
            )

            await bot.send_message(
                chat_id=int(user_id),
                text=text,
                parse_mode="Markdown",
            )

            logger.info(f"📨 Course access notification sent to user {user_id}")

        except Exception as e:
            logger.error(f"❌ Failed to send course access to user {user_id}: {e}")
            raise Exception(e)