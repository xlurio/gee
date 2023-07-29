from typing import Annotated

from fastapi import APIRouter, Depends, Path

from app.data_access.dependencies import get_unit_of_work
from app.data_access.unit_of_work import UnitOfWork

router = APIRouter(prefix="/api/places")


DUMMY_PLACES = [
    {
        "id": 1,
        "name": "Salvador Vegan Café",
        "description": "Vegan café with books and vintage music",
        "image": "/images/salvador-vegan-cafe.jpg",
        "posted_by": {
            "id": 1,
            "name": "Roberto Carlos",
            "username": "robertocarlos",
            "password": "roberto123",
        },
        "latitude": -26.3009765,
        "longitude": -48.8507455,
        "categories": [
            {"id": 1, "name": "vegan"},
            {"id": 6, "name": "lactose free"},
            {"id": 2, "name": "cafe"},
        ],
    },
    {
        "id": 2,
        "name": "Cheiro de Café",
        "description": "Gluten free coffee",
        "image": "/images/cheiro-de-cafe.jpg",
        "posted_by": {
            "id": 1,
            "name": "Pedro Manobrista",
            "username": "pedromanobrista",
            "password": "pedro123",
        },
        "latitude": -26.2928036,
        "longitude": -48.8482753,
        "categories": [{"id": 3, "name": "gluten free"}, {"id": 4, "name": "cafe"}],
    },
    {
        "id": 3,
        "name": "Veg&Tais",
        "description": "Affective vegan food. Animal-free products",
        "image": "/images/veg-e-tais.png",
        "posted_by": {
            "id": 1,
            "name": "Antônio Duro",
            "username": "antonioduro",
            "password": "antonio123",
        },
        "latitude": -26.2706992,
        "longitude": -48.8504551,
        "categories": [
            {"id": 1, "name": "vegan"},
            {"id": 5, "name": "finger food"},
            {"id": 6, "name": "lactose free"},
            {"id": 7, "name": "sandwitches"},
        ],
    },
]


@router.get("/{north}/{east}/{south}/{west}")
def list_places_by_bounds(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
    north: Annotated[float, Path(title="north bound")],
    east: Annotated[float, Path(title="east bound")],
    south: Annotated[float, Path(title="south bound")],
    west: Annotated[float, Path(title="west bound")],
):
    return {"data": uow.filter_places_by_bounds(north, east, south, west)}
