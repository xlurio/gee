import logging
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("passlib.utils.compat").setLevel(logging.ERROR)


load_dotenv()


def _get_root_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, ".."))


class Settings(BaseSettings):
    TEMPLATES_DIR: str = os.path.join(_get_root_dir(), "templates")
    STATIC_URL: str = "/static"
    STATICFILES_DIR: str = os.path.join(_get_root_dir(), "static")
    GOOGLEMAPSJS_API_KEY: str
    GOOGLEGEOCODINGAPI_API_KEY: str
    GOOGLEPLACESAPI_API_KEY: str
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    DATABASE_PROTOCOL: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    TOKEN_URL: str = "/api/token"
    SECRET_KEY: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    SENDER_EMAIL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ELASTICSEARCH_PROTOCOL: str
    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: int
    BROKER_PROTOCOL: str
    BROKER_HOST: str
    BROKER_PORT: int
    BROKER_USERNAME: str = ""
    BROKER_PASSWORD: str = ""


settings = Settings()
