from src.models import Media


async def save_media(file_name: str, file_id: str):
    await Media.create(
        name=file_name,
        file_id=file_id,
    )