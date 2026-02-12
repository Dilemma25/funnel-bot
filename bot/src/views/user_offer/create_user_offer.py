from src.models import UserOffer
from datetime import datetime
from src.models.offer import Offer


async def create_user_offer(
        user_id: int,
        offer_code: str,
        connection=None,
        discount_price: float = None,
        discount_expires_at: datetime = None,
):

    offer_query = Offer.filter(code=offer_code)

    if connection:
        offer_query = offer_query.using_db(connection)

    offer = await offer_query.first()

    if not offer:
        raise ValueError(f"Offer {offer_code} not found")

    if connection:
        user_offer = await UserOffer.create(
            user_id=user_id,
            offer_id=offer.id,
            discount_price=discount_price,
            discount_expires_at=discount_expires_at,
            using_db=connection,
        )
    else:
        user_offer = await UserOffer.create(
            user_id=user_id,
            offer_id=offer.id,
            discount_price=discount_price,
            discount_expires_at=discount_expires_at,
        )

    return user_offer