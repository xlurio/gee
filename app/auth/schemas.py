import pydantic


class TokenPayload(pydantic.BaseModel):
    sub: int | None = None

class Token(pydantic.BaseModel):
    token: str