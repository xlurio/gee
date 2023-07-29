from typing import Annotated

from elasticsearch import Elasticsearch
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.search import make_elastic_search
from app.data_access.database import SessionLocal
from app.data_access.unit_of_work import UnitOfWork


def get_session() -> Session:
    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()


def get_elastic_search() -> Elasticsearch:
    esearch = make_elastic_search()

    try:
        yield esearch
    finally:
        esearch.close()


def get_unit_of_work(
    session: Annotated[Session, Depends(get_session)],
    esearch: Annotated[Elasticsearch, Depends(get_elastic_search)],
) -> UnitOfWork:
    uow = UnitOfWork(session, esearch)

    try:
        yield uow

    finally:
        uow.rollback()
