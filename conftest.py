import os
import dotenv
import pytest

@pytest.fixture(autouse=True, scope="session")
def envs():
    dotenv.load_dotenv()

@pytest.fixture
def app_url():
    url = os.getenv("APP_URL")
    if url is None:
        raise ValueError("APP_URL не задан в .env")
    return url