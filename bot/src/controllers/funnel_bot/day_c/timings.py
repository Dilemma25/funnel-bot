from datetime import timedelta
from src.core.config import settings

IS_DEV = settings.is_dev
DEV_DELAY = 30  # секунд


class TimingsDayC:
    """Таймеры для Day B воронки"""
    # C2 таймер оффера — 30 минут
    DISCOUNT_TIMER = timedelta(seconds=DEV_DELAY if IS_DEV else 30 * 60)
