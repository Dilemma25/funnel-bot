from src.models import Offer


async def get_offer_by_code(code, connection):
    offer = await Offer.get(
        code=code,
        using_db=connection
    )

    return offer