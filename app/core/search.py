import contextlib

from elasticsearch import Elasticsearch

from app.core.config import settings


def make_elastic_search() -> Elasticsearch:
    return Elasticsearch(
        f"{settings.ELASTICSEARCH_PROTOCOL}://{settings.ELASTICSEARCH_HOST}:"
        f"{settings.ELASTICSEARCH_PORT}"
    )


@contextlib.contextmanager
def esearch_context():
    esearch = Elasticsearch(
        f"{settings.ELASTICSEARCH_PROTOCOL}://{settings.ELASTICSEARCH_HOST}:"
        f"{settings.ELASTICSEARCH_PORT}"
    )

    try:
        yield esearch

    finally:
        esearch.close()
