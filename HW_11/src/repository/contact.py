from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.entity.models import Contacts
from src.schemas.schemas import ContactSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contacts).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contacts).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contacts(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(body: ContactSchema, contact_id: int, db: AsyncSession):
    stmt = select(Contacts).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.vaccinated = body.vaccinated
        contact.description = body.description
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contacts).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
