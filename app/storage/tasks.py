from typing import BinaryIO, cast

from app.core.emails import EmailSender
from app.core.search import esearch_context
from app.core.task_queue import task_queue
from app.data_access import schemas
from app.data_access.database import SessionLocal
from app.data_access.unit_of_work import UnitOfWork
from app.local_typing import CeleryTask
from app.storage.services import ImageStorage


@task_queue.task()
def _store_place_image(place_id: int, content: bytes):
    with SessionLocal() as session:
        with esearch_context() as esearch:
            with UnitOfWork(session, esearch) as uow:
                place = uow.get_place_by_id(place_id)
                with EmailSender() as sender:
                    ImageStorage(uow, sender).store_place_image(place, content)


store_place_image = cast(CeleryTask, _store_place_image)