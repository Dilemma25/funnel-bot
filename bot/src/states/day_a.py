# from aiogram.fsm.state import StatesGroup
# from aiogram.fsm.state import State
#
#
# class DayAStates(StatesGroup):
#     """FSM states для воронки Day A"""
#
#     # A1 - Приветствие
#     a_1_greeting_sent = State()  # Отправлено приветственное сообщение с кнопкой "Ок, давай по делу"
#
#     # A2 - Видео
#     a_2_video_sent = State()  # Отправлено видео про утечки денег
#
#     # A3 - Чек-лист
#     a_3_checklist_sent = State()  # Отправлен PDF чек-лист из 20 пунктов
#     a_3_waiting_for_choice = State()  # Ждем выбора (нашел/не нашел проблемы)
#
#     # C1/C2 - Переход к квизу
#     c1_found_sent = State()  # Отправлено сообщение C1 (нашел проблемы)
#     c2_not_found_sent = State()  # Отправлено сообщение C2 (не нашел проблемы)
#
#     # A4 - Квиз (4 вопроса)
#     a_4_quiz_q1 = State()  # Вопрос 1 - как часто ешь вне дома
#     a_4_quiz_q2 = State()  # Вопрос 2 - как часто покупаешь кофе
#     a_4_quiz_q3 = State()  # Вопрос 3 - сколько подписок
#     a_4_quiz_q4 = State()  # Вопрос 4 - покупки на маркетплейсах
#
#     # A5 - Результат квиза
#     a_5_quiz_result_sent = State()  # Показан результат квиза с суммой утечек
#
#     # A6 - Кружок про жадность
#     a_6_video_note_jadnost_sent = State()  # Отправлен видеокружок V1_krujok_jadnost
#
#     # A7 - Сообщение про систему
#     a_7_system_message_sent = State()  # Отправлено сообщение A7 с кнопкой "Понятно, что дальше?"
#
#     # A8 - Кружок про метод
#     a_8_video_note_method_sent = State()  # Отправлен видеокружок V2_krujok_metod
#
#     # A9 - Предложение курса
#     a_9_offer_sent = State()  # Показано предложение A9 (оплатить/узнать подробнее)
#
#     # A9.1 - Выбрал "Узнать подробнее"
#     a_9_1_faq_requested = State()  # Юзер нажал "Узнать подробнее"
#
#     # A9.2 - FAQ отправлен
#     a_9_2_faq_sent = State()  # Отправлены FAQ сообщения (A9_2, A9_q_1-4)
#     a_9_2_waiting_for_choice = State()  # Ждем выбора (купить/отзывы)
#
#     # A9.2.1 - Повторное предложение
#     a_9_2_1_repeat_offer_sent = State()  # Отправлено повторное предложение A9_2_1
#
#     # A10 - Оплата
#     day_a_10_payment_process = State()  # Процесс оплаты начат
#     day_a_10_payment_success = State()  # Оплата успешна
#     day_a_10_payment_failed = State()  # Оплата не прошла
#
#     # Дополнительные состояния
#     day_a_reviews_sent = State()  # Отправлены отзывы (если есть)
#     day_a_completed = State()  # Воронка завершена (купил курс)
