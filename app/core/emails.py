import contextlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from types import TracebackType
from typing import cast

from app.core.config import settings
from app.data_access import models


class EmailSender(contextlib.AbstractContextManager):
    def __init__(self) -> None:
        self.__server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)

    def __exit__(
        self,
        __exc_type: type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        del __exc_type
        self.close()

        if __exc_value is None:
            return True

        raise __exc_value.with_traceback(__traceback)

    def close(self) -> None:
        self.__server.quit()
        self.__server.close()

    def notify_invalid_image(self, place: models.Place) -> None:
        message = MIMEMultipart()
        message["From"] = settings.SENDER_EMAIL
        message["To"] = cast(models.User, place.posted_by).email
        message["Subject"] = "Invalid image"
        message.attach(MIMEText(f"The image sent for {place.name} is not valid."))

        self.__send_email_to(message)

    def __send_email_to(self, message: MIMEMultipart) -> None:
        if settings.SMTP_USERNAME:
            password = settings.SMTP_PASSWORD if settings.SMTP_PASSWORD else ""
            self.__server.login(settings.SMTP_USERNAME, password)

        self.__server.sendmail(
            settings.SENDER_EMAIL, message["To"], message.as_string()
        )
