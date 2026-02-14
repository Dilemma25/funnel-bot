from enum import Enum


class DayAStates(str, Enum):
    # A1 - Приветствие
    A_1_STARTED = "day_a_1_started"

    # A2 - Видео
    A_2_VIDEO_LID_SENT = "day_a_2_video_lid_sent"

    # A3 - Чек-лист
    A_3_CHECKLIST_SENT = "day_a_3_checklist_sent"

    # C1/C2 - Переход к квизу
    C1_FOUND_SENT = "day_a_c1_found_sent"
    C2_NOT_FOUND_SENT = "day_a_c2_not_found_sent"

    # A4 - Квиз (4 вопроса)
    A_4_QUIZ_Q1 = "day_a_4_quiz_q1"
    A_4_QUIZ_Q2 = "day_a_4_quiz_q2"
    A_4_QUIZ_Q3 = "day_a_4_quiz_q3"
    A_4_QUIZ_Q4 = "day_a_4_quiz_q4"

    # A5 - Результат квиза
    A_5_QUIZ_RESULT_SENT = "day_a_5_quiz_result_sent"

    # A6 - Кружок про жадность
    A_6_VIDEO_NOTE_JADNOST_SENT = "day_a_6_video_note_jadnost_sent"

    # A7 - Сообщение про систему
    A_7_SYSTEM_MESSAGE_SENT = "day_a_7_system_message_sent"

    # A8 - Кружок про метод
    A_8_VIDEO_NOTE_METHOD_SENT = "day_a_8_video_note_method_sent"

    # A9 - Предложение курса
    A_9_OFFER_SENT = "day_a_9_offer_sent"

    # A9.1 - Выбрал "Узнать подробнее"
    A_9_1_FAQ_REQUESTED = "day_a_9_1_faq_requested"

    # A9.2 - FAQ отправлен
    A_9_2_FAQ_SENT = "day_a_9_2_faq_sent"

    A_9_1_1_REMEMBER_ABOUT_DISCOUNT = "day_a_9_1_1_remember_about_discount"

    # A9.2.1 - Повторное предложение
    A_9_2_1_REPEAT_OFFER_SENT = "day_a_9_2_1_repeat_offer_sent"

    # Дополнительные состояния
    A_9_2_2_REVIEWS_SENT = "day_a_reviews_sent"
    FINAL = "day_a_completed"

    PAYMENT_PROCESS = "day_a_payment_process"


class DayBStates(str, Enum):
    # B1 - Холодный душ
    B_1_COLD_SHOWER = "day_b_1_cold_shower"

    # B2 - Социалка
    B_2_SOCIAL_PROOF = "day_b_2_social_proof"

    # B3 - Кружок про цену промедления
    B_3_VIDEO_NOTE_DELAY_PRICE = "day_b_3_video_note_delay_price"

    # B4 - Последнее предложение
    B_4_LAST_OFFER = "day_b_4_last_offer"

    # B5 - Оффер
    B_5_OFFER = "day_b_5_offer"

    # B6.1 - Контроль ≠ ограничения
    B_6_1_CONTROL_NOT_LIMITS = "day_b_6_1_control_not_limits"

    # B6.2 - Цена "потом"
    B_6_2_PRICE_LATER = "day_b_6_2_price_later"

    # B6.3 - Инвест-блок
    B_6_3_INVEST_BLOCK = "day_b_6_3_invest_block"

    # B7 - Напоминание о таймере
    B_7_TIMER_REMINDER = "day_b_7_timer_reminder"

    # B8 - Финальный дожим
    B_8_FINAL_PUSH = "day_b_8_final_push"

    # Оплата
    DAY_B_PAYMENT_PROCESS = "day_b_payment_process"
    DAY_B_PAYMENT_SUCCESS = "day_b_payment_success"
    DAY_B_PAYMENT_FAILED = "day_b_payment_failed"

    # Завершение
    DAY_B_COMPLETED = "day_b_completed"


class DayCStates(str, Enum):
    # C1 - Заход (персональный апгрейд)
    C_1_PERSONAL_UPGRADE = "day_c_1_personal_upgrade"

    # C2 - Оффер 1990₽
    C_2_OFFER = "day_c_2_offer"

    # C3 - Конец
    C_3_END = "day_c_3_end"

    # Оплата
    DAY_C_PAYMENT_PROCESS = "day_c_payment_process"
    DAY_C_PAYMENT_SUCCESS = "day_c_payment_success"
    DAY_C_PAYMENT_FAILED = "day_c_payment_failed"

    # Завершение
    DAY_C_COMPLETED = "day_c_completed"
