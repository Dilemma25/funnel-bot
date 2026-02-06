from src.models import Media


async def get_media_by_file_code(file_code: str, offer_id):
    """Получи file_id по названию файла"""
    media = await Media.get_or_none(
        code=file_code,
        offer_id=offer_id
    )
    if not media:
        return None
    return media.file_id