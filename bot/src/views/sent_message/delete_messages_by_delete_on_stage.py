from aiogram.exceptions import TelegramBadRequest

from src.models import SentMessage
from src.safe_bot import SafeBot
from src.core.logging_config import setup_logging

logger = setup_logging(__name__, service="bot")


async def delete_message_by_delete_on_stage(user_id: int, stage: str, tag: str, bot: SafeBot) -> None:
    messages = await SentMessage.filter(
        user_id=user_id,
        tag=tag,
        delete_on_stage=stage,
        is_deleted=False,
    )

    for message in messages:
        try:
            await bot.delete_message(
                chat_id=user_id,
                message_id=message.telegram_message_id,
            )

            message.is_deleted = True

            await message.save()
            logger.info(f"Сообщение {message.telegram_message_id} удалено успешно")

        except TelegramBadRequest as e:
            # Сообщение уже удалено или не существует
            if "message to delete not found" in str(e).lower():
                message.is_deleted = True
                await message.save()
                logger.warning(
                    f"⚠️ Сообщение уже удалено | user_id={user_id} | "
                    f"message_id={message.telegram_message_id}"
                )
            else:
                logger.error(
                    f"❌ TelegramBadRequest | user_id={user_id} | "
                    f"message_id={message.telegram_message_id} | error={e}"
                )

        except Exception as e:

            logger.error(f"Сообщение {message.telegram_message_id} не удалось удалить: {e}", exc_info=True)

