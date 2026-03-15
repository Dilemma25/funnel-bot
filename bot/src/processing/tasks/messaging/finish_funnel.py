from src.models.offer import OfferCodesEnum
from src.models.user_history import EventTypeEnum
from src.models.user_offer import UserOfferStatusEnum
from src.views.user_history import create_user_history
from src.views.user_history.get_last_user_activity import get_last_user_activity
from src.views.user_offer.user_has_dropped import user_has_dropped
from src.views.user_state.update_user_state import update_user_state
from .base_messaging import BaseMessagingTask
from src.processing.tasks.preparable import PreparableTask
from src.views.user_offer import cancel_user_offer_with_status

from aiogram.types import Message


class FinishFunnelTask(BaseMessagingTask, PreparableTask):

    async def prepare(self, connection):

        user_id = self.payload["user_id"]

        is_dropped = await user_has_dropped(
            user_id=user_id,
            connection=connection,
        )

        if is_dropped:
            last_user_activity = await get_last_user_activity(
                user_id=user_id,
                connection=connection
            )

            await create_user_history(
                user_id=user_id,
                event_type=EventTypeEnum.USER_DROPPED,
                user_stage=last_user_activity.stage,
                connection=connection,
            )

            await cancel_user_offer_with_status(
                user_id=user_id,
                offer_code=OfferCodesEnum.SMART_WALLET,
                new_status=UserOfferStatusEnum.DROPPED,
                connection=connection,
            )

        else:
            await cancel_user_offer_with_status(
                user_id=user_id,
                offer_code=OfferCodesEnum.SMART_WALLET,
                new_status=UserOfferStatusEnum.COMPLETED_FREE,
                connection=connection,
            )

        await self.update_user_state(connection)

        return True

    async def execute(self) -> Message:
        keyboard = self._build_keyboard()

        message = await self.bot.send_message(
            chat_id=self.payload["user_id"],
            text=self.payload["text"],
            reply_markup=keyboard,
            parse_mode="Markdown",
            protect_content=True,
        )

        return message