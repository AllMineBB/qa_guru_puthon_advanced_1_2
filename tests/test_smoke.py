
from http import HTTPStatus
import requests


def test_status(app_url):
    response = requests.get(f"{app_url}/status")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["database"] is True


def test_users_available(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK


def test_create_and_delete_user(app_url):
    user = {
        "email": "smoke@test.com",
        "first_name": "Smoke",
        "last_name": "Test",
        "avatar": "https://example.com/avatar.jpg"
    }
    response = requests.post(f"{app_url}/api/users/", json=user)
    assert response.status_code == HTTPStatus.CREATED

    user_id = response.json()["id"]

    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK