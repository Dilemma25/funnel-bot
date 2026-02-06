from src.models import UserOffer


async def get_user_offer(user_id: int, offer_code: str, connection):
    """Получить UserOffer если существует"""
    return await (
        UserOffer
        .filter(user_id=user_id, offer__code=offer_code)
        .using_db(connection)
        .prefetch_related("payments")
        .first()
    )