from src.models import Media


async def save_media(
        file_id,
        file_code: str,
        offer_id: int,
        bot_tag: str,
        file_type: str,
        connection=None
):
    if connection:
        await Media.create(
            file_id=file_id,
            code=file_code,
            offer_id=offer_id,
            bot_tag=bot_tag,
            file_type=file_type,
            using_db=connection,
        )
    else:
        await Media.create(
            file_id=file_id,
            code=file_code,
            offer_id=offer_id,
            bot_tag=bot_tag,
            file_type=file_type,
        )