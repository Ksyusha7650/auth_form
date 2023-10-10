from datetime import datetime

from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    login: str
    password: str


class UserPayload(BaseModel):
    login: str = Field(min_length=3, max_length=127)
    password: str = Field(min_length=5, max_length=10)
