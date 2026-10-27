import json
from http import HTTPStatus

import pytest
import requests
from app.models.User import User


@pytest.fixture(scope="module")
def fill_test_data(app_url):
    with open("users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users/", json=user)
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/users/{user_id}")


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.mark.usefixtures("fill_test_data")
def test_users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK

    user_list = response.json()
    for user in user_list:
        User.model_validate(user)


@pytest.mark.usefixtures("fill_test_data")
def test_users_no_duplicates(users):
    users_ids = [user["id"] for user in users]
    assert len(users_ids) == len(set(users_ids))


def test_user(app_url, fill_test_data):
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        User.model_validate(user)


@pytest.mark.parametrize("user_id", [13])
def test_user_nonexistent_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("user_id", [-1, 0, "fafaf"])
def test_user_invalid_values(app_url, user_id):
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def test_method_not_allowed(app_url):
    response = requests.delete(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

@pytest.mark.parametrize("email", ["notanemail", "test@", "@test.com", ""])
#Говорим pytest — запусти этот тест 4 раза, каждый раз подставляя новый email из списка
def test_create_user_invalid_email(app_url, email):
    #Функция принимает два параметра — app_url из фикстуры и email из параметризации
    user = {
        "email": email, # ← сюда подставляется каждый раз новый email
        "first_name": "New",
        "last_name": "User",
        "avatar": "https://example.com/avatar.jpg"
    }
    #Каждый раз создаём словарь с невалидным email. Остальные поля одинаковые.
    response = requests.post(f"{app_url}/api/users/", json=user)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
