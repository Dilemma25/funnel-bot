class DayAStates:
    """Просто строковые константы для состояний Day A"""

    # A1 - Приветствие
    A_1_STARTED = "day_a_1_started"

    # A2 - Видео
    A_2_VIDEO_LID_SENT = "day_a_2_video_lid_sent"

    # A3 - Чек-лист
    A_3_CHECKLIST_SENT = "day_a_3_checklist_sent"
    A_3_WAITING_FOR_CHOICE = "day_a_3_waiting_for_choice"

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
    A_9_2_WAITING_FOR_CHOICE = "day_a_9_2_waiting_for_choice"

    # A9.2.1 - Повторное предложение
    A_9_2_1_REPEAT_OFFER_SENT = "day_a_9_2_1_repeat_offer_sent"

    # A10 - Оплата
    DAY_A_10_PAYMENT_PROCESS = "day_a_10_payment_process"
    DAY_A_10_PAYMENT_SUCCESS = "day_a_10_payment_success"
    DAY_A_10_PAYMENT_FAILED = "day_a_10_payment_failed"

    # Дополнительные состояния
    DAY_A_9_2_2_REVIEWS_SENT = "day_a_reviews_sent"
    DAY_A_COMPLETED = "day_a_completed"
