from fastapi import APIRouter, Request

from app.core.config import settings
from app.core.templates import templates

router = APIRouter()


@router.get("/")
def display_map(request: Request):
    return templates.TemplateResponse(
        "map.html",
        {
            "request": request,
            "maps_api_key": settings.GOOGLEMAPSJS_API_KEY,
        },
    )



