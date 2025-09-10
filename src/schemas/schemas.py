from datetime import date
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class ContactBase(BaseModel):
    # Ці поля будуть використовуватися у всіх схемах
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone_number: str = Field(pattern=r"^\+?\d{10,15}$")
    birthday: date
    other_info: str | None = None

    @field_validator("birthday")
    @classmethod
    def validate_birthday_is_not_in_future(cls, v: date):
        if v > date.today():
            raise ValueError("Birthday cannot be in the future!")
        return v


# Схема для вхідних даних при створенні контакту
# Вона успадковує ContactBase, але не має id, бо його генерує база даних.
class ContactCreate(ContactBase):
    pass


# Схема для вихідних даних
# Вона має id і model_config, бо вона відображає дані з бази даних.
class Contact(ContactBase):
    contact_id: int
    model_config = ConfigDict(from_attributes=True)
