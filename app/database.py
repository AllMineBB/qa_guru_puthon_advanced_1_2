import os
from sqlmodel import create_engine, SQLModel

engine = create_engine(os.getenv("DATABASE_ENGINE"))

SQLModel.metadata.create_all(engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)