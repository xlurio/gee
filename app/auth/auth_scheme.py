from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings

auth_scheme = OAuth2PasswordBearer(settings.TOKEN_URL)
