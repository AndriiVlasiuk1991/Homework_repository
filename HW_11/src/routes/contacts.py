from fastapi import FastAPI, Depends, HTTPException, status, Path, Request, Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import contact as repositories_contacts
from src.schemas.schemas import ContactResponse, ContactSchema


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.update_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.delete_contact(contact_id, db)
    return contact

# @router.get("/contacts", response_model=list[ContactResponse], tags=["contacts"])
# async def get_contact(db: Session = Depends(get_db)):
#     contacts = db.query(Contact).all()
#     return contacts


# @router.get("/contact/{contact_id}", response_model=ContactResponse, tags=["contacts"])
# async def get_contact_by_id(contact_id: int = Path(ge=1),
#                             db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter_by(id=contact_id).first()
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
#
#     return contact
#
#
# @router.post("/contact", response_model=ContactResponse, tags=["contacts"])
# async def create_contact(body: ContactSchema, db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter_by(email=body.email).first()
#     if contact:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact is existing")
#     contact = Contact(name=body.name, surname=body.surname, email=body.email)
#     db.add(contact)
#     db.commit()
#     return contact
#
#
# @router.put("/contact/{contact_id}", response_model=ContactResponse, tags=["contacts"])
# async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1),
#                          db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter_by(id=contact_id).first()
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
#
#     contact.name = body.name
#     contact.surname = body.surname
#     contact.email = body.email
#
#     db.commit()
#     return contact
#
#
# @router.delete("/contact/{contact_id}", response_model=ContactResponse, tags=["contacts"])
# async def delete_contact(contact_id: int = Path(ge=1),
#                          db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter_by(id=contact_id).first()
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
#
#     db.delete(contact)
#     db.commit()
#     return contact
