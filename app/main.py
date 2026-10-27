import dotenv
dotenv.load_dotenv()

import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers import status, users
from app.database.engine import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.warning("On status")
    create_db_and_tables()  # выполняется при старте
    yield                   # приложение работает здесь
                            # после yield — код при остановке (у нас его нет)
    logging.warning("On shutdown")

app = FastAPI(lifespan=lifespan)
app.include_router(status.router)
app.include_router(users.router)