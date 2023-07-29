from collections.abc import Mapping
from typing import Any, cast

from app.core.search import esearch_context
from app.core.task_queue import task_queue
from app.local_typing import CeleryTask


@task_queue.task()
def _create_or_update_document(index: str, document: Mapping[str, Any], id: str):
    with esearch_context() as esearch:
        esearch.index(index=index, document=document, id=id)


create_or_update_document = cast(CeleryTask, _create_or_update_document)