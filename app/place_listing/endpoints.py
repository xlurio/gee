from typing import Annotated

from fastapi import APIRouter, Depends, Path
from app.core import response_schemas
from app.data_access import schemas

from app.data_access.dependencies import get_unit_of_work
from app.data_access.unit_of_work import UnitOfWork

router = APIRouter(prefix="/api/places")


@router.get(
    "/{north}/{east}/{south}/{west}",
    response_model=list[schemas.Place],
    responses=response_schemas.RESPONSES,
)
def list_places_by_bounds(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
    north: Annotated[float, Path(title="north bound")],
    east: Annotated[float, Path(title="east bound")],
    south: Annotated[float, Path(title="south bound")],
    west: Annotated[float, Path(title="west bound")],
):
    """List all registered places within the passed bounds"""
    return {"data": uow.filter_places_by_bounds(north, east, south, west)}
