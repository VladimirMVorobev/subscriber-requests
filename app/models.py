
import re
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator


class RequestReason(str, Enum):
    NO_NETWORK = "нет доступа к сети"
    PHONE_NOT_WORKING = "не работает телефон"
    EMAIL_NOT_RECEIVED = "не приходят письма"


class SubscriberRequest(BaseModel):
    last_name: str
    first_name: str
    birth_date: date
    phone: str
    email: EmailStr
    reasons: list[RequestReason] = Field(min_length=1)
    problem_datetime: datetime

    @field_validator("last_name", "first_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not re.fullmatch(r"[А-ЯЁ][а-яё]*", value):
            raise ValueError(
                "Имя и фамилия должны начинаться с заглавной "
                "буквы и содержать только кириллицу"
            )
        return value

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, value: date) -> date:
        if value >= date.today():
            raise ValueError("Дата рождения должна быть в прошлом")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not re.fullmatch(r"\+7\d{10}", value):
            raise ValueError(
                "Номер телефона должен иметь формат +7XXXXXXXXXX"
            )
        return value

    @field_validator("reasons")
    @classmethod
    def validate_reasons(
        cls, value: list[RequestReason]
    ) -> list[RequestReason]:
        if len(value) != len(set(value)):
            raise ValueError("Причины обращения не должны повторяться")
        return value

    @field_validator("problem_datetime")
    @classmethod
    def validate_problem_datetime(
        cls, value: datetime
    ) -> datetime:
        if value.tzinfo is None:
            raise ValueError(
                "Укажите часовой пояс времени обнаружения проблемы"
            )
        if value > datetime.now(value.tzinfo):
            raise ValueError(
                "Время обнаружения проблемы не может быть в будущем"
            )
        return value
