from src.models import UserOfferPayment


async def mark_payment_by_yookassa_id(yookassa_payment_id: str, new_status: str, connection=None):
    """
    Пометить платёж как успешный

    Args:
        yookassa_payment_id: ID платежа из yookassa
        new_status: статус из PaymentStatusEnum которым будем помечать платеж
        connection: DB connection (опциональный)

    Returns:
        UserOfferPayment c User объект или None если не найден
    """

    query = UserOfferPayment.filter(yookassa_payment_id=yookassa_payment_id)

    if connection:
        query = query.using_db(connection)

    payment = await query.first()

    if not payment:
        return None

    payment.status = new_status

    if connection:
        await payment.save(using_db=connection)
    else:
        await payment.save()

    return payment