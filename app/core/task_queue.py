import celery

from app.core.config import settings

task_queue = celery.Celery(
    "tasks",
    broker=f"{settings.BROKER_PROTOCOL}://{settings.BROKER_USERNAME}:"
    f"{settings.BROKER_PASSWORD}@{settings.BROKER_HOST}:{settings.BROKER_PORT}//",
)
