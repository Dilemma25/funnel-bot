from src.models import Media


async def get_by_file_name(file_name: str):
    """Получи file_id по названию файла"""
    media = await Media.get_or_none(name=file_name)
    if not media:
        return None
    return media.file_id