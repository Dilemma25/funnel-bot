from src.models.payment import PaymentStatusEnum
from src.views.sent_message import delete_message_by_delete_on_stage
from .base_messaging import BaseMessagingTask
from src.processing.tasks.preparable import PreparableTask
from src.views.user_offer import remove_discount
from src.views.user_offer_payment import get_payment_with_status
from src.views.user_offer import get_user_offer

from aiogram.types import Message


class RemoveDiscountAndSendMessageTask(BaseMessagingTask, PreparableTask):

    async def prepare(self, connection):
        # ✅ Проверяем, не купил ли пользователь уже

        user_offer = await get_user_offer(
            user_id=self.payload["user_id"],
            offer_code=self.payload["offer_code"],
            connection=connection
        )

        # # Если есть успешный платёж - не снимаем скидку и не отправляем сообщение
        # successful_payment = await get_payment_with_status(user_offer.id, connection, PaymentStatusEnum.SUCCESSFUL)
        # if successful_payment:
        #     return False  # сигнал не выполнять execute()

        await remove_discount(
            user_id=self.payload["user_id"],
            offer_code=self.payload["offer_code"],
            connection=connection
        )
        return True

    async def execute(self) -> Message:
        keyboard = self._build_keyboard()

        await delete_message_by_delete_on_stage(
            user_id=self.payload["user_id"],
            stage=self.payload["message_stage"],
            tag=self.payload["message_tag"],
            bot=self.bot,
        )

        message = await self.bot.send_message(
            chat_id=self.payload["user_id"],
            text=self.payload["text"],
            reply_markup=keyboard,
            parse_mode="Markdown",
            protect_content=True,
        )

        return message