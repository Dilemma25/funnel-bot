from src.models import Media


async def save_media(file_id, file_code: str, offer_id):
    await Media.create(
        file_id=file_id,
        code=file_code,
        offer_id=offer_id,
    )