from src.models import UserOfferPayment
from src.models.payment import PaymentStatusEnum


async def get_successful_payment(user_offer_id: int, connection=None):
    """Получить успешный платёж для UserOffer"""
    query = UserOfferPayment.filter(
        user_offer_id=user_offer_id,
        status=PaymentStatusEnum.SUCCESSFUL
    )

    if connection:
        query = query.using_db(connection)

    return await query.first()