from http import HTTPStatus

from fastapi import APIRouter

from app.models.AppStatus import AppStatus
from app.main import users


# from app.models.User import

router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users))
