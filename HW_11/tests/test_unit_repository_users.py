import unittest
import pytest
from unittest.mock import MagicMock, AsyncMock, Mock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import UserSchema
from src.entity.models import User
from src.repository.users import get_user_by_username, create_user, update_token, update_avatar_url


class TestAsyncContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = User(id=1, username="test_username", email="test_email@gmail.com", password="test_password",
                         refresh_token="old_token")
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_user_by_username(self):
        body = UserSchema(username="test_username", email="test_email@gmail.com", password="password")
        email = body.email

        user_instance = User(id=1, username="test_username", email="test_email@gmail.com", password="password")

        mocked_session = MagicMock(spec=AsyncSession)
        mocked_session.execute.return_value.scalar_one_or_none = Mock(return_value=user_instance)

        result = await get_user_by_username(email, mocked_session)
        self.assertIsInstance(result, User)

    async def test_create_user(self):
        body = UserSchema(username="test_username", email="test_email@gmail.com", password="password")
        result = await create_user(body, self.session)
        self.assertIsInstance(result, User)

    async def test_update_token(self):
        new_token = "new_token"
        await update_token(self.user, new_token, self.session)

    @pytest.mark.asyncio
    async def test_confirmed_email(self):
        m = pytest.MonkeyPatch()
        m.setattr("src.repository.users.get_user_by_username", self.user)

        m.undo()

    # async def test_update_avatar_url(self):
    #     email = "test_email@gmail.com"
    #     url = "http://example.com/avatar.jpg"
    #
    #     user_instance = MagicMock()
    #     user_instance.avatar = None
    #     with patch("src.repository.users.get_user_by_username", return_value=user_instance):
    #         result = await update_avatar_url(email, url, self.session)
    #
    #     user_instance.assert_called_once()
    #     user_instance.assert_called_once_with(email, self.session)
    #     self.assertEqual(result, user_instance)
    #     self.assertEqual(user_instance.avatar, url)
    #     user_instance.commit.assert_awaited_once()
    #     user_instance.refresh.assert_awaited_once_with(user_instance)

