from typing import List, Optional
from src.controllers.schemas.task_payloads import KeyboardButton


def button(
        text: str,
        callback_data: Optional[str] = None,
        url: Optional[str] = None,
) -> KeyboardButton:
    """
    Создать кнопку (возвращает Pydantic модель)

    Args:
        text: Текст кнопки
        callback_data: Callback data для inline кнопки
        url: URL для кнопки-ссылки

    Returns:
        KeyboardButton (Pydantic модель)

    Raises:
        ValueError: Если не указан ни callback_data, ни url

    Examples:
        button("Купить", callback_data="buy")
        button("Сайт", url="https://example.com")
    """
    return KeyboardButton(
        text=text,
        callback_data=callback_data,
        url=url
    )


def keyboard(*rows: List[KeyboardButton]) -> List[List[KeyboardButton]]:
    """
    Создать клавиатуру из строк кнопок

    Args:
        *rows: Ряды кнопок (каждый ряд - список KeyboardButton)

    Returns:
        Клавиатура в формате List[List[KeyboardButton]]

    Examples:
        keyboard(
            [button("Кнопка 1", callback_data="btn1")],
            [button("Кнопка 2", callback_data="btn2"), button("Кнопка 3", callback_data="btn3")],
        )
    """
    return list(rows)


def inline_keyboard(*rows: List[KeyboardButton]) -> List[List[KeyboardButton]]:
    """
    Алиас для keyboard() (для читаемости)

    Examples:
        inline_keyboard(
            [button("Купить", callback_data="buy")],
            [button("Сайт", url="https://...")],
        )
    """
    return keyboard(*rows)