from datetime import datetime
from typing import Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime


class TokenData(BaseModel):
    email: Union[str, None] = None


class VerifyTokenResponse(BaseModel):
    valid: bool
    reason: str | None = None
