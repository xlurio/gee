from typing import cast

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.local_typing import SQLAlchemyBase

SQLALCHEMY_DATABASE_URL = (
    f"{settings.DATABASE_PROTOCOL}://{settings.DATABASE_USER}:"
    f"{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:"
    f"{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = cast(type[SQLAlchemyBase], declarative_base())
