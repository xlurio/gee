from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from app.auth.services import PasswordService
from app.data_access import schemas
from app.data_access.dependencies import get_unit_of_work
from app.data_access.unit_of_work import UnitOfWork

router = APIRouter(prefix="/api/users")


@router.post("/", response_model=schemas.User, status_code=201)
def create_user(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)], user_data: schemas.UserCreate
):
    hashed_password = PasswordService().hash_password(user_data.password)

    user = uow.create_user(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )

    try:
        uow.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    uow.refresh(user)

    return user
