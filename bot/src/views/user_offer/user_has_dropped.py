from src.controllers.user_states import DayCStates, get_state_order
from src.models.offer import OfferCodesEnum
from src.views.user_state.get_user_state import get_user_state

# Функция для проверки, отвалился ли юзер, либо дошел до финального шага воронки
# применяется только в случае, если не было успешного платежа и воронка завершилась
async def user_has_dropped(
        user_id: int,
        connection = None,
) -> bool:

    user_state = await get_user_state(
        user_id = user_id,
        offer_code=OfferCodesEnum.SMART_WALLET,
        connection=connection
    )

    return user_state.state != DayCStates.C_2_OFFER



