from http import HTTPStatus
import json
import pytest
import requests
from app.models.User import User

def test_create_user(app_url):  # ← убрать fill_test_data
    user = {
        "email": "new@test.com",
        "first_name": "New",
        "last_name": "User",
        "avatar": "https://example.com/avatar.jpg"
    }
    response = requests.post(f"{app_url}/api/users/", json=user)
    assert response.status_code == HTTPStatus.CREATED
    created = response.json()
    User.model_validate(created)
    assert created["email"] == user["email"]
    assert created["first_name"] == user["first_name"]
    requests.delete(f"{app_url}/api/users/{created['id']}")  # ← чистим за собой

@pytest.mark.parametrize("missing_field", ["email", "first_name", "last_name", "avatar"])
def test_create_user_missing_field(app_url, missing_field):
        user = {
            "email": "new@test.com",
            "first_name": "New",
            "last_name": "User",
            "avatar": "https://example.com/avatar.jpg"
        }
        del user[missing_field]
        response = requests.post(f"{app_url}/api/users/", json=user)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

@pytest.mark.parametrize("email", ["notanemail", "test@", "@test.com", ""])
def test_create_user_invalid_email(app_url, email):
    user = {
        "email": email,
        "first_name": "New",
        "last_name": "User",
        "avatar": "https://example.com/avatar.jpg"
    }
    response = requests.post(f"{app_url}/api/users/", json=user)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def test_delete_user(app_url, created_user):
    user_id = created_user["id"]
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_delete_nonexistent_user(app_url):
    response = requests.delete(f"{app_url}/api/users/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_delete_invalid_id(app_url, user_id):
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def test_update_user(app_url, created_user):
    user_id = created_user["id"]
    update_data = {"first_name": "Updated", "last_name": "Name"}
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=update_data)
    assert response.status_code == HTTPStatus.OK
    updated_user = response.json()
    assert updated_user["first_name"] == "Updated"
    assert updated_user["last_name"] == "Name"

def test_update_user_get_after(app_url, created_user):
    user_id = created_user["id"]
    requests.patch(f"{app_url}/api/users/{user_id}", json={"first_name": "CheckMe"})
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["first_name"] == "CheckMe"

def test_update_nonexistent_user(app_url):
    response = requests.patch(f"{app_url}/api/users/99999", json={"first_name": "Test"})
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_user_flow(app_url):
    # Создаём
    user = {
        "email": "flow@test.com",
        "first_name": "Flow",
        "last_name": "Test",
        "avatar": "https://example.com/avatar.jpg"
    }
    response = requests.post(f"{app_url}/api/users/", json=user)
    assert response.status_code == HTTPStatus.CREATED
    user_id = response.json()["id"]

    # Читаем
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["email"] == user["email"]

    # Обновляем
    response = requests.patch(f"{app_url}/api/users/{user_id}", json={"first_name": "Updated"})
    assert response.status_code == HTTPStatus.OK
    assert response.json()["first_name"] == "Updated"

    # Удаляем
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK

    # Проверяем что удалён
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND