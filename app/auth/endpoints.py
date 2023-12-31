from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.dependencies import get_authenticator
from app.auth.schemas import Token
from app.auth.services import Authenticator
from app.core import response_schemas
from app.core.config import settings
from app.core.templates import templates

router = APIRouter()


@router.post(
    settings.TOKEN_URL,
    response_model=Token,
    responses=response_schemas.RESPONSES
)
def generate_token(
    authenticator: Annotated[Authenticator, Depends(get_authenticator)],
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """Pass your credentials to this endpoint to generate a token"""
    return {
        "token": authenticator.authenticate(login_data.username, login_data.password)
    }


@router.get("/login")
def display_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register")
def display_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
