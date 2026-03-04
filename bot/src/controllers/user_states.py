# from enum import Enum
#
#
# class DayAStates(str, Enum):
#     A_1_STARTED = "day_a:1_started"
#     A_2_VIDEO_LID_SENT = "day_a:2_video_lid_sent"
#     A_3_CHECKLIST_SENT = "day_a:3_checklist_sent"
#
#     C1_FOUND_SENT = "day_a:c1_found_sent"
#     C2_NOT_FOUND_SENT = "day_a:c2_not_found_sent"
#
#     A_4_QUIZ_Q1 = "day_a:4_quiz_q1"
#     A_4_QUIZ_Q2 = "day_a:4_quiz_q2"
#     A_4_QUIZ_Q3 = "day_a:4_quiz_q3"
#     A_4_QUIZ_Q4 = "day_a:4_quiz_q4"
#
#     A_5_QUIZ_RESULT_SENT = "day_a:5_quiz_result_sent"
#     A_6_VIDEO_NOTE_JADNOST_SENT = "day_a:6_video_note_jadnost_sent"
#     A_7_SYSTEM_MESSAGE_SENT = "day_a:7_system_message_sent"
#     A_8_VIDEO_NOTE_METHOD_SENT = "day_a:8_video_note_method_sent"
#
#     A_9_OFFER_SENT = "day_a:9_offer_sent"
#     A_9_1_FAQ_REQUESTED = "day_a:9_1_faq_requested"
#     A_9_2_FAQ_SENT = "day_a:9_2_faq_sent"
#     A_9_1_1_REMEMBER_ABOUT_DISCOUNT = "day_a:9_1_1_remember_about_discount"
#     A_9_2_1_REPEAT_OFFER_SENT = "day_a:9_2_1_repeat_offer_sent"
#     A_9_2_2_REVIEWS_SENT = "day_a:9_2_2_reviews_sent"
#
#     PAYMENT_PROCESS = "day_a:payment_process"
#     FINAL = "day_a:completed"
#
#
# class DayBStates(str, Enum):
#     B_1_COLD_SHOWER = "day_b:1_cold_shower"
#     B_2_SOCIAL_PROOF = "day_b:2_social_proof"
#     B_3_VIDEO_NOTE_DELAY_PRICE = "day_b:3_video_note_delay_price"
#     B_4_LAST_OFFER = "day_b:4_last_offer"
#     B_5_OFFER = "day_b:5_offer"
#
#     B_6_1_CONTROL_NOT_LIMITS = "day_b:6_1_control_not_limits"
#     B_6_2_PRICE_LATER = "day_b:6_2_price_later"
#     B_6_3_INVEST_BLOCK = "day_b:6_3_invest_block"
#
#     B_7_TIMER_REMINDER = "day_b:7_timer_reminder"
#     B_8_FINAL_PUSH = "day_b:8_final_push"
#
#     DAY_B_PAYMENT_PROCESS = "day_b:payment_process"
#     DAY_B_PAYMENT_SUCCESS = "day_b:payment_success"
#     DAY_B_PAYMENT_FAILED = "day_b:payment_failed"
#
#     DAY_B_COMPLETED = "day_b:completed"
#
#
# class DayCStates(str, Enum):
#     C_1_PERSONAL_UPGRADE = "day_c:1_personal_upgrade"
#     C_2_OFFER = "day_c:2_offer"
#     C_3_END = "day_c:3_end"
#
#     DAY_C_PAYMENT_PROCESS = "day_c:payment_process"
#     DAY_C_PAYMENT_SUCCESS = "day_c:payment_success"
#     DAY_C_PAYMENT_FAILED = "day_c:payment_failed"
#
#     DAY_C_COMPLETED = "day_c:completed"

from enum import Enum


class DayAStates(str, Enum):
    """Day A stages с порядковыми номерами (1000-1999)"""

    def __new__(cls, value: str, order: int):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._order = order
        return obj

    A_1_STARTED = ("day_a:1_started", 1000)
    A_2_VIDEO_LID_SENT = ("day_a:2_video_lid_sent", 1010)
    A_3_CHECKLIST_SENT = ("day_a:3_checklist_sent", 1020)

    C1_FOUND_SENT = ("day_a:c1_found_sent", 1030)
    C2_NOT_FOUND_SENT = ("day_a:c2_not_found_sent", 1030)

    A_4_QUIZ_Q1 = ("day_a:4_quiz_q1", 1040)
    A_4_QUIZ_Q2 = ("day_a:4_quiz_q2", 1041)
    A_4_QUIZ_Q3 = ("day_a:4_quiz_q3", 1042)
    A_4_QUIZ_Q4 = ("day_a:4_quiz_q4", 1043)

    A_5_QUIZ_RESULT_SENT = ("day_a:5_quiz_result_sent", 1050)
    A_6_VIDEO_NOTE_JADNOST_SENT = ("day_a:6_video_note_jadnost_sent", 1060)
    A_7_SYSTEM_MESSAGE_SENT = ("day_a:7_system_message_sent", 1070)
    A_8_VIDEO_NOTE_METHOD_SENT = ("day_a:8_video_note_method_sent", 1080)

    A_9_OFFER_SENT = ("day_a:9_offer_sent", 1090)
    A_9_1_FAQ_REQUESTED = ("day_a:9_1_faq_requested", 1091)
    A_9_2_FAQ_SENT = ("day_a:9_2_faq_sent", 1092)
    A_9_1_1_REMEMBER_ABOUT_DISCOUNT = ("day_a:9_1_1_remember_about_discount", 1093)
    A_9_2_1_REPEAT_OFFER_SENT = ("day_a:9_2_1_repeat_offer_sent", 1094)
    A_9_2_2_REVIEWS_SENT = ("day_a:9_2_2_reviews_sent", 1095)

    PAYMENT_PROCESS = ("day_a:payment_process", 1100)
    FINAL = ("day_a:completed", 1110)

    @property
    def order(self) -> int:
        return self._order


class DayBStates(str, Enum):
    """Day B stages с порядковыми номерами (2000-2999)"""

    def __new__(cls, value: str, order: int):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._order = order
        return obj

    B_1_COLD_SHOWER = ("day_b:1_cold_shower", 2000)
    B_2_SOCIAL_PROOF = ("day_b:2_social_proof", 2010)
    B_3_VIDEO_NOTE_DELAY_PRICE = ("day_b:3_video_note_delay_price", 2020)
    B_4_LAST_OFFER = ("day_b:4_last_offer", 2030)
    B_5_OFFER = ("day_b:5_offer", 2040)

    B_6_1_CONTROL_NOT_LIMITS = ("day_b:6_1_control_not_limits", 2050)
    B_6_2_PRICE_LATER = ("day_b:6_2_price_later", 2051)
    B_6_3_INVEST_BLOCK = ("day_b:6_3_invest_block", 2052)

    B_7_TIMER_REMINDER = ("day_b:7_timer_reminder", 2060)
    B_8_FINAL_PUSH = ("day_b:8_final_push", 2070)

    DAY_B_PAYMENT_PROCESS = ("day_b:payment_process", 2080)
    DAY_B_PAYMENT_SUCCESS = ("day_b:payment_success", 2090)
    DAY_B_PAYMENT_FAILED = ("day_b:payment_failed", 2091)

    DAY_B_COMPLETED = ("day_b:completed", 2100)

    FINAL = ("day_b:final", 2900)

    @property
    def order(self) -> int:
        return self._order


class DayCStates(str, Enum):
    """Day C stages с порядковыми номерами (3000-3999)"""

    def __new__(cls, value: str, order: int):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj._order = order
        return obj

    C_1_PERSONAL_UPGRADE = ("day_c:1_personal_upgrade", 3000)
    C_2_OFFER = ("day_c:2_offer", 3010)
    C_3_END = ("day_c:3_end", 3020)

    DAY_C_PAYMENT_PROCESS = ("day_c:payment_process", 3030)
    DAY_C_PAYMENT_SUCCESS = ("day_c:payment_success", 3040)
    DAY_C_PAYMENT_FAILED = ("day_c:payment_failed", 3041)

    DAY_C_COMPLETED = ("day_c:completed", 3050)

    @property
    def order(self) -> int:
        return self._order


# ✅ Хелпер функция для получения order по строке
def get_stage_order(stage_str: str) -> int:
    # Пробуем найти в DayAStates
    try:
        return DayAStates(stage_str).order
    except ValueError:
        pass

    # Пробуем найти в DayBStates
    try:
        return DayBStates(stage_str).order
    except ValueError:
        pass

    # Пробуем найти в DayCStates
    try:
        return DayCStates(stage_str).order
    except ValueError:
        pass

    # Не найдено ни в одном enum
    return 0