import abc
from collections.abc import Mapping
from typing import Any

from sqlalchemy import (ARRAY, DECIMAL, Boolean, Column, Enum, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship

from app.data_access.constants import Categories
from app.data_access.database import Base
from app.local_typing import SQLAlchemyBase


class DictableMixin:
    def to_dict(self: SQLAlchemyBase) -> Mapping[str, Any]:
        return {
            column_name: getattr(self, column_name)
            for column_name in self.__table__.columns.keys()
        }


class PlacesToEatModel(SQLAlchemyBase, DictableMixin, metaclass=abc.ABCMeta):
    id: int


class User(Base, DictableMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    places = relationship("Place", back_populates="posted_by")


class Place(Base, DictableMixin):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    image = Column(String, nullable=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    street = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)
    latitude = Column(DECIMAL(precision=9, scale=7), nullable=True)
    longitude = Column(DECIMAL(precision=10, scale=7), nullable=True)
    categories = Column(ARRAY(Enum(Categories)), default=[])
    posted_by_id = Column(Integer, ForeignKey("users.id"))
    posted_by = relationship("User", back_populates="places")
