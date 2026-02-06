from src.models import Offer


async def create_offer(code: str, title: str, description: str, base_price: float):
    offer = await Offer.create(
        code=code,
        title=title,
        description=description,
        base_price=base_price
    )
    return offer