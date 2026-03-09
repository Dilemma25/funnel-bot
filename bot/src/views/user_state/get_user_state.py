from src.models import UserState


async def get_user_state(
        user_id: int,
        offer_code: str,
        connection=None
) -> UserState | None:
    """
    Получить UserState по user_id и offer_code

    Args:
        user_id: Telegram ID пользователя
        offer_code: Код оффера (например, "SMART_WALLET")
        connection: DB connection (optional)

    Returns:
        UserState или None если не найден
    """

    query = UserState.filter(
        user_id=user_id,
        offer__code=offer_code
    )

    if connection:
        query = query.using_db(connection)

    user_state = await query.first()

    return user_state