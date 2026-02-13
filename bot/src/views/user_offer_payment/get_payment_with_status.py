from src.models import UserOfferPayment
from typing import Literal
from typing import Optional


async def get_payment_with_status(
        user_id: int,
        offer_code: str,
        payment_status: str,
        connection=None,
        order_by: Optional[Literal["newest", "oldest"]] = None
):
    """
    Получить платёж юзера по офферу с сортировкой

    Args:
        user_id: ID пользователя
        offer_code: Код оффера
        payment_status: Статус платежа
        connection: DB connection (optional)
        order_by: Сортировка ("newest" - новые первыми, "oldest" - старые первыми)

    Returns:
        UserOfferPayment или None
    """
    query = UserOfferPayment.filter(
        user_id=user_id,
        offer__code=offer_code,
        status=payment_status
    )

    if connection:
        query = query.using_db(connection)

    # Сортировка
    if order_by == "newest":
        query = query.order_by("-created_at")  # DESC
    else:
        query = query.order_by("created_at")  # ASC

    return await query.first()