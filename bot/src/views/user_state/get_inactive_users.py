from src.models import UserState
from datetime import datetime
from datetime import timedelta
from src.controllers.user_states import DayAStates
from src.core.config import settings


DAY_A_BEFORE_OFFER = [
    DayAStates.A_1_STARTED,
    DayAStates.A_2_VIDEO_LID_SENT,
    DayAStates.A_3_CHECKLIST_SENT,
    DayAStates.C1_FOUND_SENT,
    DayAStates.C2_NOT_FOUND_SENT,
    DayAStates.A_4_QUIZ_Q1,
    DayAStates.A_4_QUIZ_Q2,
    DayAStates.A_4_QUIZ_Q3,
    DayAStates.A_4_QUIZ_Q4,
    DayAStates.A_5_QUIZ_RESULT_SENT,
    DayAStates.A_6_VIDEO_NOTE_JADNOST_SENT,
    DayAStates.A_7_SYSTEM_MESSAGE_SENT,
    DayAStates.A_8_VIDEO_NOTE_METHOD_SENT,
]


async def get_inactive_users(now: datetime):

    if settings.is_dev:
        minutes_before_send_nudge = 4
    else:
        minutes_before_send_nudge = 180

    threshold = now - timedelta(minutes=minutes_before_send_nudge)

    user_states = await UserState.filter(
        last_activity_at__lt=threshold,
        nudge_sent=False,
        state__in=DAY_A_BEFORE_OFFER, # Все стейты до офера
        user__is_message_blocked = False,
    ).prefetch_related('user').all()

    users = [us.user for us in user_states]

    return users