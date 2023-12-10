from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Contacts(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(50))
    birthday: Mapped[str] = mapped_column(String(50))
    vaccinated: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[str] = mapped_column(String(150), nullable=False)

