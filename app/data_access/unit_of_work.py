import contextlib
import logging
from collections.abc import Sequence
from types import TracebackType

from elasticsearch import Elasticsearch
from sqlalchemy.orm import Session

from app.data_access import repositories
from app.data_access.models import Place as PlaceModel
from app.data_access.models import PlacesToEatModel, User
from app.data_access.schemas import Place as PlaceSchema
from app.data_access.schemas import PlaceCreate
from app.data_access.tasks import create_or_update_document
from app.local_typing import SQLAlchemyBase


class UnitOfWork(contextlib.AbstractContextManager):
    def __init__(self, session: Session, esearch: Elasticsearch):
        self.__session = session
        self.__users = repositories.UserRepository(session)
        self.__places = repositories.PlaceRepository(session, esearch)
        self.__logger = logging.getLogger(self.__class__.__name__)

    def __enter__(self) -> "UnitOfWork":
        return super().__enter__()

    def __exit__(
        self,
        __exc_type: type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        del __exc_type
        self.rollback()

        if __exc_value is None:
            return True

        raise __exc_value.with_traceback(__traceback)

    def get_user_by_id(self, user_id: int) -> User:
        return self.__users.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> User:
        return self.__users.get_by_username(username)
    
    def get_place_by_id(self, place_id: int) -> PlaceModel:
        return self.__places.get_by_id(place_id)

    def filter_places_by_bounds(
        self, north: float, east: float, south: float, west: float
    ) -> Sequence[PlaceSchema]:
        return self.__places.filter_by_bounds(north, east, south, west)

    def create_place(self, place_data: PlaceCreate, user_id: int) -> PlaceModel:
        self.__logger.debug("Creating place '%s'", place_data.name)
        created_place = self.__places.create(place_data, user_id)
        self.__logger.info("Place '%s' created", place_data.name)

        return created_place

    def create_user(
        self, username: str, hashed_password: str, email: str = None
    ) -> User:
        self.__logger.debug("Registering user '%s'", username)
        created_user = self.__users.create(
            username=username, email=email, hashed_password=hashed_password
        )
        self.__logger.info("User '%s' registered", username)

        return created_user

    def update_place_index(self, place: PlaceModel) -> None:
        self.index(place)

    def commit_index_and_refresh(self, model_instance: SQLAlchemyBase) -> None:
        self.__session.commit()
        self.index(model_instance)
        self.__session.refresh(model_instance)

    def commit(self) -> None:
        self.__logger.debug("Committing changes")
        self.__session.commit()
        self.__logger.debug("Changes committed")

    def index(self, model_instance: PlacesToEatModel) -> None:
        create_or_update_document.delay(
            index=model_instance.__class__.__name__.lower(),
            document=model_instance.to_dict(),
            id=str(model_instance.id),
        )

    def rollback(self) -> None:
        self.__session.rollback()

    def refresh(self, model_instance: SQLAlchemyBase) -> None:
        self.__session.refresh(model_instance)
