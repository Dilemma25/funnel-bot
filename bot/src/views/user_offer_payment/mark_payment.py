from src.models import UserOfferPayment
import logging

logger = logging.getLogger(__name__)


async def mark_payment(payment_id: str, new_status: str, connection=None):
    """
    Пометить платёж как успешный

    Args:
        payment_id: ID платежа из ЮKassa
        new_status: статус из PaymentStatusEnum которым будем помечать платеж
        connection: DB connection (опциональный)

    Returns:
        UserOfferPayment объект или None если не найден
    """

    query = UserOfferPayment.filter(id=payment_id)

    if connection:
        query = query.using_db(connection)

    payment = await query.first()

    if not payment:
        logger.error(f"❌ Платёж {payment_id} не найден в БД")
        return None

    payment.status = new_status

    if connection:
        await payment.save(using_db=connection)
    else:
        await payment.save()

    # logger.info(f"✅ Платёж {payment_id} помечен как SUCCESSFUL")

    return payment