import pydantic

from app.data_access import schemas


class Address(pydantic.BaseModel):
    street: str
    number: int
    city: str
    country: str

    @classmethod
    def from_place(cls, place: schemas.PlaceBase):
        return cls(
            street=place.street,
            number=place.number,
            city=place.city,
            country=place.country,
        )
    