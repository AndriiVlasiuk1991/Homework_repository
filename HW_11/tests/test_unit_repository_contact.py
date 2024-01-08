import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.schemas import ContactSchema
from src.entity.models import Contacts, User
from src.repository.contact import get_contacts, get_all_contacts, get_contact, create_contact, update_contact, \
    delete_contact


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User(id=1, username="test_user", password="qwerty", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contacts(id=1, name="Andrii", surname="Vlasiuk", user=self.user),
                    Contacts(id=2, name="Ana", surname="Vlasiuk", user=self.user),
                    ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_get_all_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contacts(id=1, name="Andrii", surname="Vlasiuk", user=self.user),
                    Contacts(id=2, name="Ana", surname="Vlasiuk", user=self.user),
                    ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_all_contacts(limit, offset, self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact(self):
        contact = Contacts(id=1, user=self.user)

        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = contact
        self.session.execute.return_value = mocked_contact
        result = await get_contact(1, self.session, self.user)
        self.assertEqual(result, contact)

    async def test_create_contact(self):
        body = ContactSchema(name="test_name", surname="test_surname", phone="test_phone", birth_day=None,
                             vaccinated=False, description="test_description")
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contacts)

    async def test_update_contact(self):
        body = ContactSchema(name="updated_name",
                             surname="updated_surname",
                             phone="updated_phone",
                             birth_day="2022-01-01",
                             vaccinated=True,
                             description="updated_description")

        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contacts(id=1, name="old_name", surname="old_surname",
                                                                  phone="old_phone", vaccinated=False,
                                                                  description="old_description", user=self.user)
        self.session.execute.return_value = mocked_contact
        result = await update_contact(body, 1, self.session, self.user)
        self.assertEqual(result.name, "updated_name")
        self.assertEqual(result.surname, "updated_surname")
        self.assertEqual(result.phone, "updated_phone")
        self.assertTrue(result.vaccinated)
        self.assertEqual(result.description, "updated_description")

    async def test_delete_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contacts(id=1, user=self.user)
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        self.assertIsInstance(result, Contacts)
