from enum import Enum


class DayAStates(str, Enum):
    A_1_STARTED = "day_a:1_started"
    A_2_VIDEO_LID_SENT = "day_a:2_video_lid_sent"
    A_3_CHECKLIST_SENT = "day_a:3_checklist_sent"

    C1_FOUND_SENT = "day_a:c1_found_sent"
    C2_NOT_FOUND_SENT = "day_a:c2_not_found_sent"

    A_4_QUIZ_Q1 = "day_a:4_quiz_q1"
    A_4_QUIZ_Q2 = "day_a:4_quiz_q2"
    A_4_QUIZ_Q3 = "day_a:4_quiz_q3"
    A_4_QUIZ_Q4 = "day_a:4_quiz_q4"

    A_5_QUIZ_RESULT_SENT = "day_a:5_quiz_result_sent"
    A_6_VIDEO_NOTE_JADNOST_SENT = "day_a:6_video_note_jadnost_sent"
    A_7_SYSTEM_MESSAGE_SENT = "day_a:7_system_message_sent"
    A_8_VIDEO_NOTE_METHOD_SENT = "day_a:8_video_note_method_sent"

    A_9_OFFER_SENT = "day_a:9_offer_sent"
    A_9_1_FAQ_REQUESTED = "day_a:9_1_faq_requested"
    A_9_2_FAQ_SENT = "day_a:9_2_faq_sent"
    A_9_1_1_REMEMBER_ABOUT_DISCOUNT = "day_a:9_1_1_remember_about_discount"
    A_9_2_1_REPEAT_OFFER_SENT = "day_a:9_2_1_repeat_offer_sent"
    A_9_2_2_REVIEWS_SENT = "day_a:9_2_2_reviews_sent"

    PAYMENT_PROCESS = "day_a:payment_process"
    FINAL = "day_a:completed"


class DayBStates(str, Enum):
    B_1_COLD_SHOWER = "day_b:1_cold_shower"
    B_2_SOCIAL_PROOF = "day_b:2_social_proof"
    B_3_VIDEO_NOTE_DELAY_PRICE = "day_b:3_video_note_delay_price"
    B_4_LAST_OFFER = "day_b:4_last_offer"
    B_5_OFFER = "day_b:5_offer"

    B_6_1_CONTROL_NOT_LIMITS = "day_b:6_1_control_not_limits"
    B_6_2_PRICE_LATER = "day_b:6_2_price_later"
    B_6_3_INVEST_BLOCK = "day_b:6_3_invest_block"

    B_7_TIMER_REMINDER = "day_b:7_timer_reminder"
    B_8_FINAL_PUSH = "day_b:8_final_push"

    DAY_B_PAYMENT_PROCESS = "day_b:payment_process"
    DAY_B_PAYMENT_SUCCESS = "day_b:payment_success"
    DAY_B_PAYMENT_FAILED = "day_b:payment_failed"

    DAY_B_COMPLETED = "day_b:completed"


class DayCStates(str, Enum):
    C_1_PERSONAL_UPGRADE = "day_c:1_personal_upgrade"
    C_2_OFFER = "day_c:2_offer"
    C_3_END = "day_c:3_end"

    DAY_C_PAYMENT_PROCESS = "day_c:payment_process"
    DAY_C_PAYMENT_SUCCESS = "day_c:payment_success"
    DAY_C_PAYMENT_FAILED = "day_c:payment_failed"

    DAY_C_COMPLETED = "day_c:completed"
