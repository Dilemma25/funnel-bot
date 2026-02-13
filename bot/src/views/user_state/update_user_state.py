from src.models import UserState
from src.models import Offer

async def update_user_state(
    user_id: int,
    offer_code: str,
    state = None,
    last_activity_at =  None,
    nudge_sent = None,
    connection = None,
):
    """
    Обновление UserState по user_id и offer_code.
    Если connection передан — поиск и сохранение через него.
    """

    # Сначала ищем оффер по коду
    if connection:
        offer = await Offer.filter(code=offer_code).using_db(connection).first()
    else:
        offer = await Offer.filter(code=offer_code).first()

    if not offer:
        return None  # Оффер с таким кодом не найден

    # Теперь ищем UserState по user_id и найденному offer.id
    if connection:
        user_state = await UserState.filter(user_id=user_id, offer_id=offer.id).using_db(connection).first()
    else:
        user_state = await UserState.filter(user_id=user_id, offer_id=offer.id).first()

    if not user_state:
        return None  # UserState не найден

    # Обновляем поля, если переданы
    if state is not None:
        user_state.state = state
    if last_activity_at is not None:
        user_state.last_activity_at = last_activity_at
    if nudge_sent is not None:
        user_state.nudge_sent = nudge_sent

    # Сохраняем через connection или без него
    if connection:
        await user_state.save(using_db=connection)
    else:
        await user_state.save()

    return user_state