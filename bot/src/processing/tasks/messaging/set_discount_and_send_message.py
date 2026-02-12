from src.processing.tasks.messaging.base_messaging import BaseMessagingTask
from src.processing.tasks.preparable import PreparableTask
from src.views.user_offer import set_discount


class SetDiscountAndSendMessageTask(BaseMessagingTask, PreparableTask):

    async def prepare(self, connection) -> None:
        """
            Устанавливает скидку + отправляет сообщение с оффером

            Payload:
            {
                "user_id": int,
                "text": str,
                "keyboard": list,  # опционально
                "offer_code": str,
                "discount_price": float,
                "discount_duration": timedelta (в секундах через .total_seconds())
            }
        """
        await set_discount(
            user_id=self.payload["user_id"],
            offer_code=self.payload["offer_code"],
            discount_price=self.payload["discount_price"],
            discount_duration=self.payload["discount_duration"],
            connection=connection
        )


    async def execute(self):

        keyboard = self._build_keyboard()

        await self.bot.send_message(
            chat_id=self.payload["user_id"],
            text=self.payload["text"],
            reply_markup=keyboard,
            parse_mode="Markdown",
        )