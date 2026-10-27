import json
import requests
import os

import dotenv
import pytest


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")

@pytest.fixture(scope="module")
# Фикстура запускается один раз на весь модуль (файл с тестами). Все тесты в файле используют одни и те же данные.
def fill_test_data(app_url):
    with open("users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users/", json=user)
        api_users.append(response.json())
    # Перебираем каждого пользователя из файла → отправляем POST запрос → сохраняем ответ сервера (с id) в api_users.

    user_ids = [user["id"] for user in api_users]
    yield user_ids
    # Вытаскиваем только id всех созданных пользователей.
    # yield — возвращаем user_ids в тест. Тест получает список [1, 2, 3, ...] и работает с ним.
    # Всё что после yield — это teardown — выполняется после теста.

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/users/{user_id}")
    # После того как тест закончился — удаляем всех созданных пользователей. Чистим базу после себя.

@pytest.fixture
def created_user(app_url):
    user = {
        "email": "test@test.com",
        "first_name": "Test",
        "last_name": "User",
        "avatar": "https://example.com/avatar.jpg"
    }
    response = requests.post(f"{app_url}/api/users/", json=user)
    user_data = response.json()
    yield user_data
    requests.delete(f"{app_url}/api/users/{user_data['id']}")