from src.models import UserOffer
from src.models import UserOfferPayment

async def get_user_offer_with_payments(user_id: int, offer_code: str, connection=None):
    """Получить UserOffer если существует"""
    if connection:
        user_offer = await UserOffer.filter(user_id=user_id, offer__code=offer_code).using_db(connection).first()
    else:
        user_offer = await UserOffer.filter(user_id=user_id, offer__code=offer_code).first()

    if user_offer:

        if connection:
            # подтягиваем платежи через user и offer
            payments = await UserOfferPayment.filter(
                user_id=user_offer.user.id,
                offer_id=user_offer.offer.id
            ).using_db(connection)
        else:
            payments = await UserOfferPayment.filter(
                user_id=user_offer.user.id,
                offer_id=user_offer.offer.id
            )

        user_offer.payments = payments

    return await user_offer