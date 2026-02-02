from aiogram.fsm.state import StatesGroup
from aiogram.fsm.state import State


class DayAStates(StatesGroup):
    starting_day_a = State()
    waiting_for_checklist_choice = State()  # A3 - выбор кнопки (нашел/не нашел проблемы)
    quiz_q1 = State()  # вопрос 1
    quiz_q2 = State()  # вопрос 2
    quiz_q3 = State()  # вопрос 3
    quiz_q4 = State()  # вопрос 4
    quiz_result= State() # результат опросника
    waiting_for_offer_choice = State()  # A9 - выбор (оплатить/узнать подробнее)
    waiting_for_faq_choice = State()  # A9.2 - выбор (купить/отзывы)