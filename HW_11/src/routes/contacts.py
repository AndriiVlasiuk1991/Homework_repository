from fastapi import Depends, HTTPException, status, Path, Query, APIRouter
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User, Role, Contacts
from src.repository import contact as repositories_contacts
from src.schemas.schemas import ContactResponse, ContactSchema
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix="/contacts", tags=["contacts"])

access_to_route_all = RoleAccess([Role.administrator, Role.moderator])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0), name: str = Query(None),
                       surname: str = Query(None), email: str = Query(None),
                       db: AsyncSession = Depends(get_db),
                       user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts function is a GET request that returns all contacts in the database.
    It can be filtered by name, surname and email. It also has pagination capabilities.

    :param limit: int: Limit the number of results returned
    :param ge: Specify a minimum value for the limit parameter
    :param le: Limit the number of results returned
    :param offset: int: Specify the number of records to skip
    :param ge: Specify that the limit must be greater than or equal to 10
    :param name: str: Filter the contacts by name
    :param surname: str: Filter contacts by surname
    :param email: str: Filter the contacts by email
    :param db: AsyncSession: Get a database connection from the pool
    :param user: User: Get the current user from the database
    :return: A list of contacts,
    :doc-author: Trelent
    """
    query = select(Contacts)
    if name:
        query = query.where(Contacts.name == name)
    if surname:
        query = query.where(Contacts.surname == surname)
    if email:
        query = query.where(Contacts.email == email)

    query = query.where(Contacts.user == user)
    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/all", response_model=list[ContactResponse], dependencies=[Depends(access_to_route_all)])
async def get_all_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0), name: str = Query(None),
                           surname: str = Query(None), email: str = Query(None),
                           db: AsyncSession = Depends(get_db)):
    """
    The get_all_contacts function returns a list of contacts.

    :param limit: int: Limit the number of results returned
    :param ge: Specify that the limit must be greater than or equal to 10
    :param le: Limit the amount of contacts that can be returned at once
    :param offset: int: Skip the first offset number of records
    :param ge: Specify that the limit must be greater than or equal to 10
    :param name: str: Filter the contacts by name
    :param surname: str: Filter the contacts by surname
    :param email: str: Filter the contacts by email
    :param db: AsyncSession: Get the database session
    :return: A list of contacts
    :doc-author: Trelent
    """
    query = select(Contacts)
    if name:
        query = query.where(Contacts.name == name)
    if surname:
        query = query.where(Contacts.surname == surname)
    if email:
        query = query.where(Contacts.email == email)

    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/upcoming_birthdays", response_model=list[ContactResponse], dependencies=[Depends(access_to_route_all)])
async def get_upcoming_birthdays(db: AsyncSession = Depends(get_db),
                                 user: User = Depends(auth_service.get_current_user)):
    """
    The get_upcoming_birthdays function returns a list of contacts with upcoming birthdays.

    :param db: AsyncSession: Get the database session
    :param user: User: Get the current user
    :return: A list of tuples
    :doc-author: Trelent
    """
    query = select(Contacts, User).join(User)

    current_date = func.current_date()

    # Використовуємо date_part для отримання місяця та дня
    birth_month = func.date_part('month', Contacts.birth_day)
    birth_day = func.date_part('day', Contacts.birth_day)

    # Знаходимо різницю в датах за місяць та день
    date_diff_expr = func.abs(birth_month - func.date_part('month', current_date)) + \
                     func.abs(birth_day - func.date_part('day', current_date))

    query = query.where(date_diff_expr <= 7, Contacts.user_id == user.id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):

    contact = await repositories_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactSchema: Validate the request body
    :param db: AsyncSession: Pass the database session to the repository
    :param user: User: Get the current user from the auth_service
    :return: A contactschema object
    :doc-author: Trelent
    """
    contact = await repositories_contacts.create_contact(body, db, user)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.update_contact(body, contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    contact = await repositories_contacts.delete_contact(contact_id, db, user)
    return contact
