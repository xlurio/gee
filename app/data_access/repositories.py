import abc
from collections.abc import Sequence
import traceback

from elasticsearch import Elasticsearch
import pydantic
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from app.core.exceptions import NoUserForIdException, NoUserForUsernameException
from app.data_access.models import Place as PlaceModel
from app.data_access.models import PlacesToEatModel, User
from app.data_access.schemas import Place as PlaceSchema
from app.data_access.schemas import PlaceCreate


class Repository(abc.ABC):
    MODEL: type[PlacesToEatModel]
    _session: Session

    def _get_query(self) -> Query[User]:
        return self._session.query(self.__class__.MODEL)


class UserRepository(Repository):
    MODEL = User

    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, user_id: int) -> User:
        possible_user = self._get_query().filter_by(id=user_id).first()

        if possible_user is None:
            raise NoUserForIdException(f"No user found for id '{user_id}'")

        return possible_user

    def get_by_username(self, username: str) -> User:
        possible_user = self._get_query().filter_by(username=username).first()

        if possible_user is None:
            raise NoUserForUsernameException(f"No user found for username '{username}'")

        return possible_user

    def create(self, username: str, hashed_password: str, email: str = None) -> User:
        user: User = self.__class__.MODEL(
            username=username, email=email, hashed_password=hashed_password
        )
        self._session.add(user)

        return user


class PlaceRepository(Repository):
    MODEL = PlaceModel

    def __init__(self, session: Session, eseach: Elasticsearch) -> None:
        self._session = session
        self.__esearch = eseach

    def create(self, place_data: PlaceCreate, user_id: User) -> PlaceModel:
        place: PlaceModel = self.__class__.MODEL(
            **place_data.model_dump(), posted_by_id=user_id
        )
        self._session.add(place)

        return place

    def get_by_id(self, place_id: int) -> PlaceModel:
        return self._get_query().get(place_id)

    def filter_by_bounds(
        self, north: float, east: float, south: float, west: float
    ) -> Sequence[PlaceModel]:
        documents = self.__esearch.search(
            index=self.__class__.MODEL.__name__.lower(),
            body={
                "query": {
                    "bool": {
                        "must": [
                            {"range": {"latitude": {"gte": west, "lte": east}}},
                            {"range": {"longitude": {"gte": south, "lte": north}}},
                        ]
                    }
                }
            },
        )["hits"]["hits"]

        try:
            return [
                PlaceSchema.model_validate(document["_source"])
                for document in documents
            ]

        except pydantic.ValidationError as error:
            traceback.print_exc()
            print(error.errors())
            print(documents)
            raise error
