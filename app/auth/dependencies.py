from typing import Annotated

from fastapi import Depends

from app.auth.auth_scheme import auth_scheme
from app.auth.services import Authenticator, PasswordService, TokenService
from app.data_access.dependencies import get_unit_of_work
from app.data_access.models import User
from app.data_access.unit_of_work import UnitOfWork


def get_current_user(
    token: Annotated[str, Depends(auth_scheme)],
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
) -> User:
    return TokenService(uow).get_user_by_token(token)


def get_token_service(
        uow: Annotated[UnitOfWork, Depends(get_unit_of_work)]
    ):
    return TokenService(uow)


def get_authenticator(uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
        password_service: Annotated[PasswordService, Depends()],
        token_service: Annotated[TokenService, Depends(get_token_service)],
    ):
    return Authenticator(uow, password_service, token_service)