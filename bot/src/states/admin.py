from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    waiting_for_file = State()
    waiting_for_file_name = State()