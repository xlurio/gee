import contextlib
from types import TracebackType

import requests

from app.core.config import settings
from app.data_access import schemas
from app.place_creation.schemas import Address


class GeoCoder(contextlib.AbstractContextManager):
    GEOCODING_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"
    PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json"

    def __init__(self) -> None:
        self.__session = requests.Session()

    def __enter__(self) -> "GeoCoder":
        return super().__enter__()

    def __exit__(
        self,
        __exc_type: type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        del __exc_type
        self.close()

        if __exc_value is None:
            return True

        raise __exc_value.with_traceback(__traceback)

    def close(self) -> None:
        self.__session.close()

    def locate(self, address: Address) -> schemas.Coordinates:
        place_id = self.__get_place_id(address)
        coordinates_data = self.__session.get(
            self.__class__.GEOCODING_API_URL,
            params={
                "key": settings.GOOGLEGEOCODINGAPI_API_KEY,
                "place_id": place_id,
            },
        ).json()["results"][0]["geometry"]["location"]

        return schemas.Coordinates(
            latitude=coordinates_data["lat"], longitude=coordinates_data["lng"]
        )

    def __get_place_id(self, address: Address) -> str:
        return self.__session.get(
            self.__class__.PLACES_API_URL,
            params={
                "key": settings.GOOGLEPLACESAPI_API_KEY,
                "input": f"{address.number} {address.street}, {address.city}, {address.country}"
            },
        ).json()["predictions"][0]["place_id"]
