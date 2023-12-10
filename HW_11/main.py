import time

from fastapi import FastAPI, Depends, HTTPException, status, Path, Request

from src.database.db import get_db
from src.routes import contacts

from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

# from db import get_db
# from middlewares import CustomHeaderMiddleware
# from models import Contact, ContactInfo
# from schemas import ContactResponse, ContactSchema, ContactInfoResponse, ContactInfoSchema

app = FastAPI()

app.include_router(contacts.router, prefix="/api")


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        # Здійснюємо запит
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response
#
#
# # contacts
# app.add_middleware(CustomHeaderMiddleware)


# @app.get("/contacts", response_model=list[ContactResponse], tags=["contacts"])
# async def get_contact(db: Session = Depends(get_db)):
#     contacts = db.query(Contact).all()
#     return contacts


# @app.get("/contact/{contact_id}", response_model=ContactResponse, tags=["contacts"])
# async def get_contact_by_id(contact_id: int = Path(ge=1),
#                             db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter_by(id=contact_id).first()
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
#
#     return contact
#
#
# @app.post("/contact", response_model=ContactResponse, tags=["contacts"])
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
# @app.put("/contact/{contact_id}", response_model=ContactResponse, tags=["contacts"])
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
# @app.delete("/contact/{contact_id}", response_model=ContactResponse, tags=["contacts"])
# async def delete_contact(contact_id: int = Path(ge=1),
#                          db: Session = Depends(get_db)):
#     contact = db.query(Contact).filter_by(id=contact_id).first()
#     if contact is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
#
#     db.delete(contact)
#     db.commit()
#     return contact
#
#
# # contact_info
# @app.get("/contacts_info", response_model=list[ContactInfoResponse], tags=["contacts_info"])
# async def get_contact_info(db: Session = Depends(get_db)):
#     contacts_info = db.query(ContactInfo).all()
#     return contacts_info
#
#
# @app.get("/contact_info/{contact_info_id}", response_model=ContactInfoResponse, tags=["contacts_info"])
# async def get_contact_info_by_id(contacts_info_id: int = Path(ge=1),
#                             db: Session = Depends(get_db)):
#     contacts_info = db.query(ContactInfo).filter_by(id=contacts_info_id).first()
#     if contacts_info is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
#
#     return contacts_info
#
#
# @app.post("/contact_info", response_model=ContactInfoResponse, tags=["contacts_info"])
# async def create_contact_info(body: ContactInfoSchema, db: Session = Depends(get_db)):
#     contacts_info = ContactInfo(**body.model_dump())
#     db.add(contacts_info)
#     db.commit()
#     return contacts_info
#
#
# @app.put("/contact_info/{contact_info_id}", response_model=ContactInfoResponse, tags=["contacts_info"])
# async def update_contact_info(body: ContactInfoSchema, contact_info_id: int = Path(ge=1),
#                          db: Session = Depends(get_db)):
#     contacts_info = db.query(ContactInfo).filter_by(id=contact_info_id).first()
#     if contacts_info is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
#
#     contacts_info.phone = body.phone
#     contacts_info.birthday = body.birthday
#     contacts_info.vaccinated = body.vaccinated
#     contacts_info.update_at = body.update_at
#     contacts_info.description = body.description
#
#     db.commit()
#     return contacts_info
#
#
# @app.delete("/contact_info/{contact_info_id}", response_model=ContactInfoResponse, tags=["contacts_info"])
# async def delete_contact_info(contact_info_id: int = Path(ge=1),
#                          db: Session = Depends(get_db)):
#     contact_info = db.query(ContactInfo).filter_by(id=contact_info_id).first()
#     if contact_info is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
#
#     db.delete(contact_info)
#     db.commit()
#     return contact_info
