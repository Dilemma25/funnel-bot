from src.models import UserOfferPayment
from src.models.payment import PaymentStatusEnum


async def get_successful_payment(user_offer_id: int, connection):
    """Получить успешный платёж для UserOffer"""
    return await UserOfferPayment.filter(
        user_offer_id=user_offer_id,
        status=PaymentStatusEnum.SUCCESSFUL
    ).using_db(connection).first()