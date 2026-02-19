from yookassa import Configuration
from yookassa import Payment
from yookassa.domain.common import SecurityHelper
from yookassa.domain.response import PaymentResponse

from src.core.config import settings
from src.core.logging_config import setup_logging
import uuid


logger = setup_logging(__name__, service="payment_service")

# Configuration.account_id = settings.shop_id
# Configuration.secret_key = settings.shop_secret_key

Configuration.configure(
    account_id=settings.shop_id,
    secret_key=settings.shop_secret_key,
)

class PaymentService:
    @staticmethod
    def check_ip(client_ip: str) -> bool:
        try:
            return SecurityHelper().is_ip_trusted(client_ip)

        except Exception as e:
            logger.error(f"Error checking IP: {e}")
            return False

    @staticmethod
    async def create_payment(user_id, amount, description):
        """Создать платеж (работает и в test, и в prod)"""

        idempotence_key = str(uuid.uuid4())

        payment = Payment.create({
            "amount": {
                "value": f"{amount}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/@ToDo25Bot"
            },
            "capture": True,
            "test": settings.is_dev,  # ← ЯВНО указываем тестовый режим (опционально)
            "description": description,
            "metadata": {
                "user_id": user_id,
                "source": "telegram_bot"
            },
        }, idempotence_key)

        return {
            "payment_id": payment.id,
            "confirmation_url": payment.confirmation.confirmation_url,
            "status": payment.status,
            "amount": amount,
            "created_at": payment.created_at,
        }

    # @staticmethod
    # async def check_payment_status(payment_id: str) -> dict:
    #     """
    #     Проверить статус платежа
    #
    #     Args:
    #         payment_id: ID платежа из ЮKassa
    #
    #     Returns:
    #         dict со статусом
    #     """
    #
    #     payment = Payment.find_one(payment_id)
    #
    #     return {
    #         "payment_id": payment.id,
    #         "status": payment.status,  # "pending", "waiting_for_capture", "succeeded", "canceled"
    #         "paid": payment.paid,  # True/False
    #         "amount": float(payment.amount.value) if payment.amount else 0,
    #         "user_id": payment.metadata.get("user_id") if payment.metadata else None,
    #         "created_at": payment.created_at,
    #     }

    @staticmethod
    async def get_payment_info(payment_id: str) -> PaymentResponse:
        """
        Проверить статус платежа

        Args:
            payment_id: ID платежа из ЮKassa

        Returns:
            dict со статусом
        """

        payment = Payment.find_one(payment_id)

        return payment

    @staticmethod
    async def close_payment(yookassa_payment_id: str):
        """
        :param yookassa_payment_id: ID платежа из Юкассы
        :return: is_closed: операция закрытия платежа проведена успешно/неуспешно
        """
        try:

            payment = Payment.cancel(yookassa_payment_id)

            return {
                "payment_id": payment.id,
                "status": payment.status,
                "cancelled": True,
            }

        except Exception as e:
            error_message = str(e)

            # Платеж уже завершен
            if "succeeded" in error_message.lower():
                logger.warning(f"⚠️ Платеж {yookassa_payment_id} уже оплачен, нельзя отменить")
                return {"payment_id": yookassa_payment_id, "canceled": False, "reason": "already_paid"}

            # Платеж уже отменен
            if "canceled" in error_message.lower():
                logger.warning(f"⚠️ Платеж {yookassa_payment_id} уже отменен")
                return {"payment_id": yookassa_payment_id, "canceled": True, "reason": "already_canceled"}

            # Другая ошибка
            logger.error(f"❌ Ошибка отмены: {e}")
            return {"payment_id": yookassa_payment_id, "canceled": False, "error": error_message}