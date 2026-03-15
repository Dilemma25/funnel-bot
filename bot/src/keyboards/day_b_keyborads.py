from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


keyboard_b2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Понятно. Что с полным пакетом?", callback_data="day_b:b3:delay_cost")],
    ]
)

keyboard_b4 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📋 Посмотреть структуру курса", callback_data="day_b:b5:cost_of_delay")],
    ]
)

keyboard_b5 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Забрать за 2 490 ₽", callback_data="day_b:buy")],
        [InlineKeyboardButton(text="Есть вопросы", callback_data="day_b:b6_1:control_not_equal_limitation")],
    ]
)

keyboard_b6 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Забираю", callback_data="day_b:b_5:offer")],
    ]
)

keyboard_b8 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Беру полный пакет", callback_data="day_b:buy")],
    ]
)


