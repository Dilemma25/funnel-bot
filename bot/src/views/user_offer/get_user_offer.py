from src.models import UserOffer
from src.models import UserOfferPayment

async def get_user_offer(user_id: int, offer_code: str, connection=None):
    """Получить UserOffer если существует"""
    query = UserOffer.filter(user_id=user_id, offer__code=offer_code)

    if connection:
        query = query.using_db(connection)

    return await query.first()