from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


keyboard_A1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ок, давай по делу", callback_data="day_a:a1:start")],
    ]
)

keyboard_A3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Нашёл(ла) несколько пунктов про себя", callback_data="day_a:a3:found"),
            InlineKeyboardButton(text="Пока не вижу явных проблем", callback_data="day_a:a3:not_found"),
        ],
    ]
)

keyboard_quiz_1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Никогда", callback_data="a4:q1_v1")],
        [InlineKeyboardButton(text="1-2 раза в неделю", callback_data="a4:q1_v2")],
        [InlineKeyboardButton(text="3-4 раза в неделю", callback_data="a4:q1_v3")],
        [InlineKeyboardButton(text="Почти каждый день", callback_data="a4:q1_v4")],
    ]
)

keyboard_quiz_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пару раз в месяц", callback_data="a4:q2_v1")],
        [InlineKeyboardButton(text="Пару раз в неделю", callback_data="a4:q2_v2")],
        [InlineKeyboardButton(text="Почти каждый день", callback_data="a4:q2_v3")],
        [InlineKeyboardButton(text="Каждый день", callback_data="a4:q2_v4")],
    ]
)
keyboard_quiz_3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Нет платных подписок", callback_data="a4:q3_v1")],
        [InlineKeyboardButton(text="1-2 подписки", callback_data="a4:q3_v2")],
        [InlineKeyboardButton(text="3-5 подписок", callback_data="a4:q3_v3")],
        [InlineKeyboardButton(text="Даже не знаю, сколько", callback_data="a4:q3_v4")],
    ]
)

keyboard_quiz_4 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Иногда покупаю что-то по случаю", callback_data="a4:q4_v1")],
        [InlineKeyboardButton(text="Пару мелочей в неделю", callback_data="a4:q4_v2")],
        [InlineKeyboardButton(text="Через день что-нибудь заказываю", callback_data="a4:q4_v3")],
        [InlineKeyboardButton(text="Очень часто, особенно акции", callback_data="a4:q4_v4")],
    ]
)