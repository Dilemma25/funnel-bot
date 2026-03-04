import os
from datetime import timedelta

from src.core.config import settings

# Определяем режим работы
IS_DEV = settings.is_dev

# Базовые таймеры для DEV режима
DEV_DELAY = 30  # секунд


class DayATimings:
    """Таймеры для Day A воронки"""

    # A2 → A3: Отправка чек-листа PDF после видео
    A2_TO_A3 = timedelta(seconds=DEV_DELAY if IS_DEV else 30)

    #Отправка клавиатуры после пдф
    A2_TO_A2_KB = timedelta(seconds=DEV_DELAY if IS_DEV else 30)

    # A5 → A6: Отправка кружка после результата квиза
    A5_TO_A6 = timedelta(seconds=DEV_DELAY if IS_DEV else 50)

    # A6 → A7: Отправка аналогии + формулы после кружка
    A6_TO_A7 = timedelta(seconds=DEV_DELAY if IS_DEV else 50)

    # A8 → A9: Предложение курса
    A8_TO_A9 = timedelta(seconds=DEV_DELAY if IS_DEV else 30)

    DISCOUNT_TIMER = timedelta(seconds=130 if IS_DEV else 30)

    #Если нажал на оплату, но не оплатил, напоминаем о таймере
    I1_TO_A9_1_1 = timedelta(seconds=70 if IS_DEV else 30)

    #Возврат к оферу после FAQ
    A9_2_TO_A9_2_1 = timedelta(seconds=DEV_DELAY if IS_DEV else 30)




class Timings:
    """Человекопонятные названия таймеров"""

    CHECKLIST_DELAY = DayATimings.A2_TO_A3
    CHECKLIST_KEYBOARD_DELAY = DayATimings.A2_TO_A2_KB

    VIDEO_NOTE_DELAY = DayATimings.A5_TO_A6
    SYSTEM_MESSAGE_DELAY = DayATimings.A6_TO_A7

    OFFER_DELAY = DayATimings.A8_TO_A9

    REMEMBER_ABOUT_DISCOUNT = DayATimings.I1_TO_A9_1_1
    RETURN_TO_OFFER = DayATimings.A9_2_TO_A9_2_1

    DISCOUNT_TIMER = DayATimings.DISCOUNT_TIMER


# def print_timings():
#     """Выводит все таймеры (для отладки)"""
#     mode = "DEV" if IS_DEV else "PRODUCTION"
#     print(f"\n=== Day A Timings ({mode}) ===")
#
#     for attr_name in dir(DayATimings):
#         if not attr_name.startswith('_'):
#             value = getattr(DayATimings, attr_name)
#             if isinstance(value, timedelta):
#                 print(f"{attr_name}: {value.total_seconds():.0f}s")
#     print()
#
#
# if __name__ == "__main__":
#     print_timings()