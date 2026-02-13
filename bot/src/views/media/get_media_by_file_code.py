from src.models import Media
from src.models.offer import Offer


async def get_media_by_file_code(file_code: str, offer_code: str, connection=None):
    """Получи file_id по названию файла и названию офера"""

    offer_query = Offer.filter(code=offer_code)

    if connection:
        offer_query = offer_query.using_db(connection)

    offer = await offer_query.first()

    if not offer:
        raise ValueError(f"Offer {offer_code} not found")

    query = Media.filter(code=file_code, offer_id=offer.id)

    if connection:
        query = query.using_db(connection)

    media = await query.first()

    if not media:
        return None

    return media.file_id