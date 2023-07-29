from typing import cast
from app.core.search import esearch_context

from app.core.task_queue import task_queue
from app.data_access import models
from app.data_access.database import SessionLocal
from app.data_access.unit_of_work import UnitOfWork
from app.local_typing import CeleryTask
from app.place_creation.schemas import Address
from app.place_creation.services import GeoCoder


@task_queue.task()
def _locate_address(place_id: int) -> None:
    with SessionLocal() as session:
        with esearch_context() as esearch:
            with UnitOfWork(session, esearch) as uow:
                place = uow.get_place_by_id(place_id)

                with GeoCoder() as geocoder:
                    coordinate = geocoder.locate(Address.from_place(place))

                place.latitude = coordinate.latitude
                place.longitude = coordinate.longitude
                uow.commit()
                uow.index(place)


locate_address = cast(CeleryTask, _locate_address)