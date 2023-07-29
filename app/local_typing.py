import abc
from collections.abc import Mapping
from typing import Any

from sqlalchemy import MetaData


class SQLAlchemyTable(abc.ABC):

    columns: Mapping[str, Any]


class SQLAlchemyBase(abc.ABC):

    metadata: MetaData
    __table__: SQLAlchemyTable


class CeleryTask(abc.ABC):

    @abc.abstractmethod
    def delay(self, *args, **kwargs):
        raise NotImplementedError