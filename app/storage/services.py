import contextlib
import logging
import pathlib
import uuid
import tempfile
from PIL import Image

from app.core.config import settings
from app.core.emails import EmailSender
from app.data_access.models import Place
from app.data_access.unit_of_work import UnitOfWork


class ImageStorage:
    def __init__(self, unit_of_work: UnitOfWork, email_sender: EmailSender) -> None:
        self.__uow = unit_of_work
        self.__email_sender = email_sender
        self.__logger = logging.getLogger(self.__class__.__name__)

    def store_place_image(self, place: Place, content: bytes) -> None:
        try:
            with tempfile.TemporaryFile() as file:
                file.write(content)
                image = Image.open(file)

        except IOError:
            self.__logger.error("Invalid image")
            self.__email_sender.notify_invalid_image(place)

        else:
            self.__store_image(place, content, image.format if image.format else "jpg")

    def __store_image(self, place: Place, content: bytes, image_format: str) -> None:
        output_filename = f"place_image_{place.id}_{uuid.uuid4()}.{image_format}"
        output_path = (
            pathlib.Path(settings.STATICFILES_DIR)
            .joinpath("uploads")
            .joinpath(output_filename)
        )
        output_path.write_bytes(content)
        place.image = f"{settings.STATIC_URL}/uploads/{output_filename}"
        self.__uow.commit()
        self.__uow.index(place)
