from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, EmailStr


class UserRequest(BaseModel):
    login: EmailStr
    password: str


class UserPayload(BaseModel):
    login: str = Field(min_length=3, max_length=127)
    password: str = Field(min_length=5, max_length=10)


class TokenPayload:
    def __init__(self, sub: str, exp: int, **kwargs: Any):
        self.sub = sub
        self.exp = exp

