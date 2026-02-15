from src.models import UserState
from src.views.user_log import create_user_log
from src.models.user_log import EventTypeEnum

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

    if connection:
        user_state = await UserState.filter(user_id=user_id, offer__code=offer_code).using_db(connection).first()
    else:
        user_state = await UserState.filter(user_id=user_id, offer__code=offer_code).first()

    if not user_state:
        return None  # UserState не найден

    # Обновляем поля, если переданы
    if state is not None:
        user_state.state = state
    if last_activity_at is not None:
        user_state.last_activity_at = last_activity_at
    if nudge_sent is not None:
        user_state.nudge_sent = nudge_sent

    # Сохраняем через connection или без него, а так же логируем
    if connection:
        await user_state.save(using_db=connection)

        await create_user_log(
            user_id=user_id,
            event_type=EventTypeEnum.STAGE_ENTERED,
            user_stage=state,
            connection=connection,
        )
    else:
        await user_state.save()

        await create_user_log(
            user_id=user_id,
            event_type=EventTypeEnum.STAGE_ENTERED,
            user_stage=state,
        )

    return user_state