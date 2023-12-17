from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from src.schemas.user import UserResponse


class ContactSchema(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: str
    birth_day: date | None
    vaccinated: Optional[bool] = False
    description: str


class ContactResponse(ContactSchema):
    id: int = 1
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None

    class Config:
        from_attributes = True
