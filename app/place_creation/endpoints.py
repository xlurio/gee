from typing import Annotated

from fastapi import APIRouter, Depends, File, Request, UploadFile

from app.auth.dependencies import get_current_user
from app.core import response_schemas
from app.core.templates import templates
from app.data_access import models, schemas
from app.data_access.constants import Categories
from app.data_access.dependencies import get_unit_of_work
from app.data_access.unit_of_work import UnitOfWork
from app.place_creation.dependencies import get_geocoder
from app.place_creation.schemas import Address
from app.place_creation.services import GeoCoder
from app.place_creation.tasks import locate_address
from app.storage.tasks import store_place_image

router = APIRouter()


@router.post(
    "/api/places",
    response_model=schemas.Place,
    status_code=201,
    responses=response_schemas.RESPONSES,
)
async def create_place(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
    curr_user: Annotated[models.User, Depends(get_current_user)],
    place_data: Annotated[schemas.PlaceCreate, Depends(schemas.PlaceCreate.as_form())],
    place_image: Annotated[UploadFile | None, File()] = None,
):
    """Mark a new place in the map"""
    place = uow.create_place(place_data, curr_user.id)
    uow.commit_index_and_refresh(place)

    if place_image:
        store_place_image.delay(place.id, await place_image.read())
        locate_address.delay(place.id)

    return place


@router.get("/create-place")
def display_create_place_form(request: Request):
    return templates.TemplateResponse(
        "create-place.html", {"request": request, "categories": Categories}
    )
