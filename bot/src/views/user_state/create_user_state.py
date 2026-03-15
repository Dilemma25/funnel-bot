from src.models import UserState


async def create_user_state(user_id: int, offer_id: str, connection = None):
    if connection is None:
        await UserState.create(
            user_id=user_id,
            offer_id=offer_id,
        )
    else:
        await UserState.create(
            user_id=user_id,
            offer_id=offer_id,
            using_db=connection
        )