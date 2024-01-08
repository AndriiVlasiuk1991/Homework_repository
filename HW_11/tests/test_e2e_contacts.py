from unittest.mock import Mock, patch
import pytest
from src.services.auth import auth_service


def test_get_contacts(client, get_token):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0


def test_create_contact(client, get_token):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("api/contacts", headers=headers,
                               json={"name": "test_name", "surname": "test_surname", "phone": "test_phone",
                                     "birth_day": None,
                                     "vaccinated": False, "description": "test_description"})
        assert response.status_code == 201, response.text
        data = response.json()
        assert "id" in data
        assert data["name"] == "test_name"
        assert data["surname"] == "test_surname"
        assert data["phone"] == "test_phone"
        assert data["birth_day"] is None
        assert data["vaccinated"] is False
        assert data["description"] == "test_description"
