import pydantic


class TokenPayload(pydantic.BaseModel):
    sub: int | None = None