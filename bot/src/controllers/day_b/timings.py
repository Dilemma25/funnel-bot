from datetime import timedelta
from src.core.config import settings

IS_DEV = settings.is_dev
DEV_DELAY = 30  # секунд


class DayBTimings:
    """Таймеры для Day B воронки"""
    # B3 → B4 (через 2 минуты)
    B3_TO_B4 = timedelta(seconds=DEV_DELAY if IS_DEV else 2 * 60)

    # B6.1 → B6.2 (через 1 минуту)
    B6_1_TO_B6_2 = timedelta(seconds=DEV_DELAY if IS_DEV else 60)

    # B6.2 → B6.3 (через 1 минуту)
    B6_2_TO_B6_3 = timedelta(seconds=DEV_DELAY if IS_DEV else 60)

    # B5 таймер оффера — 6 часов
    OFFER_TIMER = timedelta(seconds=DEV_DELAY if IS_DEV else 6 * 60 * 60)


    DISCOUNT = timedelta(seconds=DEV_DELAY if IS_DEV else 6 * 60 * 60)

    DISCOUNT_REMINDER = timedelta(seconds=DEV_DELAY if IS_DEV else 3 * 60 * 60)

    DISCOUNT_FINAL_REMINDER = timedelta(seconds=DEV_DELAY if IS_DEV else int(5.5 * 60 * 60))