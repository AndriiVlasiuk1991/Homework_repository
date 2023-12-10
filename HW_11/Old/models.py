from sqlalchemy import Column, Integer, String, func, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Boolean
from sqlalchemy.orm import relationship
from db import Base, engine


class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(150), unique=True, index=True)


class ContactInfo(Base):
    __tablename__ = "contact_info"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(50))
    birthday = Column(String(50))
    vaccinated = Column(Boolean, default=False)
    created_at = Column('created_at', DateTime, default=func.now())
    update_at = Column('update_at', DateTime, default=func.now())
    description = Column(String(150), nullable=False)
    contact_id = Column(Integer, ForeignKey("contact.id"), index=True)
    contact = relationship(argument="Contact", backref="contact_info")


Base.metadata.create_all(bind=engine)
