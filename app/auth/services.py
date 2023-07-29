import datetime
import logging

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.auth.constants import ALGORITHM
from app.auth.schemas import TokenPayload
from app.core.config import settings
from app.core.exceptions import NoUserForUsernameException
from app.data_access.models import User
from app.data_access.unit_of_work import UnitOfWork


class TokenService:
    def __init__(self, uow: UnitOfWork):
        self.__uow = uow
        self.__logger = logging.getLogger(self.__class__.__name__)

    def get_user_by_token(self, token: str) -> User:
        self.__logger.debug("Getting user by token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            token_data = TokenPayload(**payload)

        except (jwt.JWTError, ValidationError):
            self.__logger.info("Invalid token")
            raise HTTPException(
                status_code=403, detail="Could not validate credentials"
            )

        user = self.__try_to_get_user_by_id(token_data.sub)
        self.__logger.info("User %d successfully retrieved", user.id)

        return user

    def generate_token(self, user_id: int) -> str:
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return jwt.encode(
            {"exp": expiration_time, "sub": str(user_id)},
            settings.SECRET_KEY,
            algorithm=ALGORITHM,
        )

    def __try_to_get_user_by_id(self, user_id: int) -> User:
        try:
            return self.__uow.get_user_by_id(user_id)
        except Exception:
            self.__logger.info("No user was found for id %d", user_id)
            raise HTTPException(status_code=400, detail="User not found")


class PasswordService:
    def __init__(self) -> None:
        self.__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.__logger = logging.getLogger(self.__class__.__name__)

    def hash_password(self, password: str) -> str:
        self.__logger.debug("Hashing password")
        return self.__pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        self.__logger.debug("Verifying password")
        does_match = self.__pwd_context.verify(plain_password, hashed_password)
        self.__logger.info("Password verification result: %s", does_match)

        return does_match


class Authenticator:
    def __init__(
        self,
        uow: UnitOfWork,
        password_service: PasswordService,
        token_service: TokenService,
    ) -> None:
        self.__uow = uow
        self.__password_service = password_service
        self.__token_service = token_service

    def authenticate(self, username: str, password: str) -> User:
        try:
            user = self.__uow.get_user_by_username(username)

        except NoUserForUsernameException:
            raise HTTPException(status_code=400, detail="User not found")

        else:
            self.__verify_user_activation(user)
            self.__verify_password(password, user.hashed_password)

            return self.__token_service.generate_token(user.id)

    def __verify_user_activation(self, user: User) -> None:
        if not user.is_active:
            raise HTTPException(status_code=400, detail="User is not active")

    def __verify_password(self, plain_password: str, hashed_password: str) -> None:
        if not self.__password_service.verify_password(plain_password, hashed_password):
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
