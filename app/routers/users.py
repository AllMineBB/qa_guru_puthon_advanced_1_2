from http import HTTPStatus
from typing import Iterable

from fastapi import APIRouter, HTTPException

from app.database import users
from app.models.User import User, UserCreate, UserUpdate

router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.get("/", status_code=HTTPStatus.OK)
def get_users() -> Iterable[User]:
    return users.get_users()


@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate) -> User:
    return users.create_user(User.model_validate(user.model_dump(mode='json')))


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: User) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)


@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
# Функция принимает user_id — FastAPI автоматически конвертирует из URL в int. Если передать "fafaf" — конвертация не удастся → 422 автоматически.
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    # Проверяем что id не отрицательный и не ноль. Если -1 или 0 — бросаем 422.
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    # Ищем пользователя в базе. Если не нашли — 404.
    users.delete_user(user_id)
    return {"message": "User deleted"}
    # Только если все проверки прошли — удаляем из базы и возвращаем сообщение об успехе.
    # 1. id валидный? (не 0, не отрицательный) → иначе 422
    # 2. пользователь существует? → иначе 404
    # 3. удаляем → 200