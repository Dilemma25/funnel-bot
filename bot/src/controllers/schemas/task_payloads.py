from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from typing import Optional
from typing import List
from datetime import datetime


class KeyboardButton(BaseModel):
    """Кнопка клавиатуры"""
    text: str
    callback_data: Optional[str] = None
    url: Optional[str] = None

    @field_validator('callback_data', 'url', mode='before')
    def check_button_type(cls, v, info):
        """Проверка, что указан хотя бы один тип кнопки"""
        all_values = info.data

        if not v and not all_values.get('url') and not all_values.get('callback_data'):
            raise ValueError('Button must have either callback_data or url')
        return v


class BaseTaskPayload(BaseModel):
    """Базовая схема payload для всех тасок"""
    user_id: int = Field(..., description="ID пользователя Telegram")
    # ===== Трекинг сообщений для удаления =====
    message_tag: str = Field(
        ...,
        description="Тег сообщения для группировки (funnel, course, etc)"
    )

    message_stage: str = Field(
        ...,
        description="На каком этапе отправлено сообщение"
    )

    delete_at: datetime = Field(
        ...,
        description="Точное время удаления сообщения (datetime)"
    )

    delete_on_stage: str = Field(
        ...,
        description="Удалить сообщение при переходе на указанный stage"
    )

    class Config:
        # Разрешить дополнительные поля (для гибкости)
        extra = "allow"  # или "allow" если нужна гибкость


class MessageTaskPayload(BaseTaskPayload):
    """Payload для отправки простого сообщения"""
    text: str = Field(..., min_length=1, max_length=4096, description="Текст сообщения")
    keyboard: Optional[List[List[KeyboardButton]]] = Field(None, description="Inline клавиатура")
    parse_mode: str = Field(default="Markdown", description="Режим парсинга")

    @field_validator('keyboard')
    def validate_keyboard(cls, v):
        """Проверка, что клавиатура не пустая"""
        if v is not None and len(v) == 0:
            raise ValueError('Keyboard cannot be empty')
        return v

class NewDayMessageTaskPayload(MessageTaskPayload):
    offer_code: str = Field(..., description="Код оффера")

class DocumentTaskPayload(BaseTaskPayload):
    """Payload для отправки документа"""
    text: Optional[str] = Field(None, max_length=1024, description="Caption для документа")
    file_id: str = Field(..., description="Telegram file_id документа")
    keyboard: Optional[List[List[KeyboardButton]]] = None


class VideoTaskPayload(BaseTaskPayload):
    """Payload для отправки видео"""
    file_id: str = Field(..., description="Telegram file_id видео")
    caption: Optional[str] = Field(None, max_length=1024)
    keyboard: Optional[List[List[KeyboardButton]]] = None


class VideoNoteTaskPayload(BaseTaskPayload):
    """Payload для отправки видео-кружка"""
    file_id: str = Field(..., description="Telegram file_id видео-кружка")


class SetDiscountTaskPayload(MessageTaskPayload):
    """Payload для установки скидки + отправки сообщения"""
    offer_code: str = Field(..., description="Код оффера")
    discount_price: float = Field(..., gt=0, description="Цена со скидкой")
    discount_duration: float = Field(..., gt=0, description="Длительность скидки в секундах")

    @field_validator('discount_price', mode='before')
    def validate_price(cls, v):
        """Проверка, что цена разумная"""
        if v > 100000:
            raise ValueError('Price too high')
        return v


class RemoveDiscountTaskPayload(MessageTaskPayload):
    """Payload для снятия скидки + отправки сообщения"""
    offer_code: str = Field(..., description="Код оффера")

class FinishFunnelTaskPayload(MessageTaskPayload):
    offer_code: str = Field(..., description="Код оффера")