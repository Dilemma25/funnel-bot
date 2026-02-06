from .base_messaging import BaseMessagingTask
from src.views.user_offer import remove_discount


class RemoveDiscountAndSendMessageTask(BaseMessagingTask):

    async def prepare(self, connection):
        """Убираем скидку в транзакции"""
        # ✅ Проверяем, не купил ли пользователь уже
        from src.views.user_offer_payment import get_successful_payment
        from src.views.user_offer import get_user_offer

        user_offer = await get_user_offer(
            user_id=self.payload["user_id"],
            offer_code=self.payload["offer_code"],
            connection=connection
        )

        # Если есть успешный платёж - не снимаем скидку и не отправляем сообщение
        successful_payment = await get_successful_payment(user_offer.id, connection)
        if successful_payment:
            return False  # сигнал не выполнять execute()

        await remove_discount(
            user_id=self.payload["user_id"],
            offer_code=self.payload["offer_code"],
            connection=connection
        )
        return True

    async def execute(self):
        """Отправка вне транзакции"""
        await self.bot.send_message(
            chat_id=self.payload["user_id"],
            text=self.payload["text"],
        )