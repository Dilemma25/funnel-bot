from src.models import UserOffer
from datetime import datetime


async def create_user_offer(
        user_id: int,
        offer_id: int,
        connection,
        discount_price: float = None,
        discount_expires_at: datetime = None,
):
    user_offer = await UserOffer.create(
        user_id=user_id,
        offer_id=offer_id,
        discount_price=discount_price,
        discount_expires_at=discount_expires_at,
        using_db=connection,
    )
    return user_offer