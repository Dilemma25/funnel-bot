from src.models import Media
from typing import List


async def get_media_by_prefix(
        prefix: str,
        offer_code: str,
        connection=None
) -> List[Media]:
    """
    Получить все медиа-файлы по префиксу file_code

    Args:
        prefix: Префикс file_code (например, "lesson_1_module_1")
        offer_code: Код оффера
        connection: DB connection (optional)

    Returns:
        List[Media] — список файлов

    Examples:
        get_media_by_prefix("lesson_1_module_1", "SMART_WALLET")
        → [
            Media(file_code="lesson_1_module_1_video", ...),
            Media(file_code="lesson_1_module_1_calculator", ...),
            Media(file_code="lesson_1_module_1_check_list", ...)
        ]
    """

    query = Media.filter(
        code__startswith=prefix,  # ← Фильтр по префиксу
        offer__code=offer_code
    ).order_by("code") # для того, что бы для уроков где несколько видео
                        # с code lesson_2_module_1_video_1 lesson_2_module_1_video_2 доставать по порядку
    if connection:
        query = query.using_db(connection)

    media_files = await query.all()

    return media_files