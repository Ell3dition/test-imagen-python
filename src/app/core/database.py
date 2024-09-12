# Standard Library
import json

# External
from sqlmodel import Session, SQLModel, create_engine

# Project
from app.core.config import (
    MYSQL_AQUA_PASSWORD,
    MYSQL_AQUA_SERVER,
    MYSQL_AQUA_USER,
    MYSQL_DIVE_DB,
)

DATABASE_URL = f"mysql+pymysql://{MYSQL_AQUA_USER}:{MYSQL_AQUA_PASSWORD}@{MYSQL_AQUA_SERVER}/{MYSQL_DIVE_DB}"
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
