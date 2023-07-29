import decimal
from collections.abc import Sequence
from typing import Type

import pydantic
from fastapi import Form

from app.data_access.constants import Categories


class UserBase(pydantic.BaseModel):
    username: str
    email: pydantic.EmailStr


class UserCreate(UserBase):
    password: str
    password_confirmation: str

    @pydantic.model_validator(mode="after")
    def check_passwords_match(self):
        does_passwords_match = self.password == self.password_confirmation

        if does_passwords_match:
            return self

        raise pydantic.ValidationError("Passwords don't match")


class User(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


class PlaceBase(pydantic.BaseModel):
    name: str
    description: str = ""
    street: str
    number: int
    city: str
    country: str
    categories: Sequence[Categories] = pydantic.Field(default_factory=list)


class PlaceCreate(PlaceBase):
    pass

    @classmethod
    def as_form(cls) -> Type["PlaceCreateForm"]:
        cls.__signature__ = cls.__signature__.replace(
            parameters=[
                p.replace(default=Form()) for p in cls.__signature__.parameters.values()
            ]
        )

        return cls


class PlaceCreateForm(PlaceCreate.as_form()):
    pass


class Place(PlaceBase):
    id: int
    posted_by_id: int
    image: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    class Config:
        from_attributes = True


class Coordinates(pydantic.BaseModel):
    latitude: decimal.Decimal
    longitude: decimal.Decimal