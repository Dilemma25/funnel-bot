from src.models import UserOfferPayment


async def get_payment_with_status(
        user_id: int,
        offer_code: str,
        payment_status: str,
        connection=None
):
    """Получить успешный платёж юзера по офферу"""

    query = UserOfferPayment.filter(
        user_id=user_id,
        offer__code=offer_code,
        status=payment_status
    )

    if connection:
        query = query.using_db(connection)

    return await query.first()