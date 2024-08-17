from typing import Optional

from pydantic import BaseModel


class AllTokenResponse(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class RefreshToken(BaseModel):
    refresh_token: str
