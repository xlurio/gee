from app.place_creation.services import GeoCoder


def get_geocoder() -> GeoCoder:
    geocoder = GeoCoder()

    try:
        yield geocoder

    finally:
        geocoder.close()