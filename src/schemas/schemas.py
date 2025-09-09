from datetime import date
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class ContactBase(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone_number: str = Field(pattern=r"^\+?\d{10,15}$")
    birthday: date
    other_info: str | None = None

    @field_validator("birthday")
    @classmethod  # V2 validators must be class methods
    def validate_birthday_is_not_in_future(cls, v: date):
        if v > date.today():
            raise ValueError("Birthday cannot be in the future!")
        return v


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class Contact(ContactBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
