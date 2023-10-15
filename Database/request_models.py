from typing import Any
from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    login: EmailStr
    password: str
    code: str


class TokenPayload:
    def __init__(self, sub: str, exp: int, **kwargs: Any):
        self.sub = sub
        self.exp = exp

