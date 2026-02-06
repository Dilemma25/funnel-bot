from src.models import UserOfferPayment
from src.models.payment import PaymentStatusEnum
import logging

logger = logging.getLogger(__name__)


async def mark_as_successful(payment_id: str, connection):
    """
    Пометить платёж как успешный

    Args:
        payment_id: ID платежа из ЮKassa
        connection: DB connection (обязательный)

    Returns:
        UserOfferPayment объект или None если не найден
    """

    payment = await UserOfferPayment.filter(
        id=payment_id
    ).using_db(connection).first()

    if not payment:
        logger.error(f"❌ Платёж {payment_id} не найден в БД")
        return None

    if payment.status == PaymentStatusEnum.SUCCESSFUL:
        logger.info(f"ℹ️ Платёж {payment_id} уже успешный")
        return payment

    payment.status = PaymentStatusEnum.SUCCESSFUL
    await payment.save(using_db=connection)

    logger.info(f"✅ Платёж {payment_id} помечен как SUCCESSFUL")

    return payment