from yookassa import Configuration
from yookassa import Payment

from src.core.config import config

import uuid

Configuration.account_id = config['SHOP_ID']
Configuration.secret_key = config['SHOP_SECRET_KEY']

class PaymentService:

    @staticmethod
    async def create_payment(user_id, amount, description):
        """Создать платеж (работает и в test, и в prod)"""

        idempotence_key = str(uuid.uuid4())

        payment = Payment.create({
            "amount": {
                "value": f"{amount}.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/@ToDo25Bot"
            },
            "capture": True,
            "test": True,  # ← ЯВНО указываем тестовый режим (опционально)
            "description": description,
            "metadata": {
                "user_id": user_id,
                "source": "telegram_bot"
            }
        }, idempotence_key)

        return {
            "payment_id": payment.id,
            "confirmation_url": payment.confirmation.confirmation_url,
            "status": payment.status,
            "amount": amount
        }

    @staticmethod
    async def check_payment_status(payment_id: str) -> dict:
        """
        Проверить статус платежа

        Args:
            payment_id: ID платежа из ЮKassa

        Returns:
            dict со статусом
        """

        payment = Payment.find_one(payment_id)

        return {
            "payment_id": payment.id,
            "status": payment.status,  # "pending", "waiting_for_capture", "succeeded", "canceled"
            "paid": payment.paid,  # True/False
            "amount": float(payment.amount.value) if payment.amount else 0,
            "user_id": payment.metadata.get("user_id") if payment.metadata else None
        }