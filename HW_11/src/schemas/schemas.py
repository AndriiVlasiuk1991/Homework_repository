from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.schemas.user import UserResponse


class ContactSchema(BaseModel):
    name: str
    surname: str
    phone: str
    birth_day: date | None
    vaccinated: Optional[bool] = False
    description: str


class ContactResponse(ContactSchema):
    id: int = 1
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None

    model_config = ConfigDict(from_attributes = True)  # noqa

