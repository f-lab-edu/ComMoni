from pydantic import BaseModel

from app.api.auth.token_util import JwtTokenType


class Token(BaseModel):
    """
    token schema
    """
    value: str
    type: JwtTokenType


class TokenSet(BaseModel):
    """
    token set(access/refresh)
    """
    access_token: str
    refresh_token: str
