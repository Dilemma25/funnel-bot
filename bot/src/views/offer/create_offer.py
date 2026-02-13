from src.models import Offer


async def create_offer(code: str, title: str, description: str, base_price: float, connection=None):
    if connection:
        offer = await Offer.create(
            code=code,
            title=title,
            description=description,
            base_price=base_price,
            using_db=connection
        )
    else:
        offer = await Offer.create(
            code=code,
            title=title,
            description=description,
            base_price=base_price
        )

    return offer