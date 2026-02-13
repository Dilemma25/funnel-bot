from src.models import Offer


async def get_offer_by_code(code, connection=None):
    query = Offer.filter(code=code)

    if connection:
        query = query.using_db(connection)

    return await query.first()