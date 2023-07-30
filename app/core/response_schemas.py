import pydantic


class HttpErrorMessage(pydantic.BaseModel):
    detail: str


RESPONSES = {
    400: {"model": HttpErrorMessage},
    403: {"model": HttpErrorMessage},
}
