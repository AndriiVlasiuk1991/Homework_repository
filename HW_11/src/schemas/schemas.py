
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ContactSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday: str = Field(min_length=6, max_length=25)
    vaccinated: Optional[bool] = False
    description: str


class ContactResponse(ContactSchema):
    id: int = 1

    class Config:
        from_attributes = True


