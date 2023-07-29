import logging

from sqlalchemy import text
from tenacity import (after_log, before_log, retry, stop_after_attempt,
                      wait_fixed)
from app.core.search import make_elastic_search

from app.data_access.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def initiate_db_session() -> None:
    try:
        session = SessionLocal()
        session.execute(text("SELECT 1"))

    except Exception as exception:
        logging.getLogger(initiate_db_session.__name__).error(exception)
        raise


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def initiate_elasticsearch() -> None:
    try:
        if not make_elastic_search().ping():
            raise Exception("Elasticsearch is not responding")

    except Exception as exception:
        logging.getLogger(initiate_elasticsearch.__name__).error(exception)
        raise


if __name__ == "__main__":
    logger.info("Initializing database session")
    initiate_db_session()
    logger.info("Database session initialized")

    logger.info("Initializing Elastic Search")
    initiate_elasticsearch()
    logger.info("Elastic Search initialized")
