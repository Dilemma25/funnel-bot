from datetime import datetime
from typing import List, Optional
from src.models.payment import UserOfferPayment, PaymentStatusEnum


async def get_pending_payments(threshold: datetime, limit: Optional[int] = 20) -> List[UserOfferPayment]:
    """
    Получить список pending платежей старше указанного порога времени.

    Args:
        threshold: Сколько времени назад должен быть создан платеж, чтобы считаться "старым"
        limit: Максимальное количество платежей для выборки (default=20)

    Returns:
        Список объектов UserOfferPayment
    """

    query = UserOfferPayment.filter(
        status=PaymentStatusEnum.PENDING,
        created_at__lte=threshold
    )

    if limit:
        query = query.limit(limit)

    pending_payments = await query.all()

    if not pending_payments:
        return []

    return pending_payments