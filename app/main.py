from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.auth.endpoints import router as auth_router
from app.core.config import settings
from app.map_display.endpoints import router as map_display_router
from app.place_creation.endpoints import router as place_creation_router
from app.place_listing.endpoints import router as place_listing_router
from app.user_creation.endpoints import router as user_creation_router

app = FastAPI()
app.mount(
    settings.STATIC_URL, StaticFiles(directory=settings.STATICFILES_DIR), name="static"
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(map_display_router)
app.include_router(place_listing_router)
app.include_router(place_creation_router)
app.include_router(user_creation_router)
app.include_router(auth_router)
