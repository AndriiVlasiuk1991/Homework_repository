from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.entity.models import Contacts, User
from src.schemas.schemas import ContactSchema


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    """
    The get_contacts function returns a list of contacts for the user.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of rows to skip
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Filter the contacts by user
    :return: A list of contacts
    :doc-author: Trelent
    """
    stmt = select(Contacts).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    """
    The get_all_contacts function returns a list of all contacts in the database.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of rows to skip
    :param db: AsyncSession: Pass in the database session
    :return: A list of contacts
    :doc-author: Trelent
    """
    stmt = select(Contacts).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    """
    The get_contact function returns a contact from the database.

    :param contact_id: int: Specify the id of the contact to be retrieved
    :param db: AsyncSession: Pass the database session into the function
    :param user: User: Ensure that the user is only able to access their own contacts
    :return: The contact object if it exists, otherwise none
    :doc-author: Trelent
    """
    stmt = select(Contacts).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactSchema: Validate the request body
    :param db: AsyncSession: Pass the database session into the function
    :param user: User: Get the user that is logged in
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contacts(**body.model_dump(exclude_unset=True), user=user)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(body: ContactSchema, contact_id: int, db: AsyncSession, user: User):
    """
    The update_contact function updates a contact in the database.
        Args:
            body (ContactSchema): The contact to update.
            db (AsyncSession): A database session object.

    :param body: ContactSchema: Get the data from the request body
    :param contact_id: int: Get the contact from the database
    :param db: AsyncSession: Connect to the database
    :param user: User: Get the user id from the token
    :return: A contact object
    :doc-author: Trelent
    """
    stmt = select(Contacts).filter_by(id=contact_id, user=user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.name = body.name
        contact.surname = body.surname

        contact.phone = body.phone
        contact.birth_day = body.birth_day
        contact.vaccinated = body.vaccinated
        contact.description = body.description
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    """
    The delete_contact function deletes a contact from the database.

    :param contact_id: int: Specify the contact to delete
    :param db: AsyncSession: Pass in the database session
    :param user: User: Ensure that the user is only deleting their own contacts
    :return: The contact that was deleted
    :doc-author: Trelent
    """
    stmt = select(Contacts).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
