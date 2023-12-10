from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ContactSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr


class ContactResponse(ContactSchema):
    id: int = 1

    class Config:
        from_attributes = True


class ContactInfoBase(BaseModel):
    phone: int
    birthday: str = Field(min_length=6, max_length=25)
    vaccinated: Optional[bool] = False
    created_at: datetime
    update_at: datetime
    description: str


class ContactInfoSchema(ContactInfoBase):
    contact_id: int = Field(default=1, ge=1)


class ContactInfoResponse(ContactInfoBase):
    id: int = 1
    contact: ContactResponse

    class Config:
        from_attributes = True
