from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """
    access token schema
    """
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class LoginRequestParam(BaseModel):
    """
    login에 필요한 정보
    """
    host_id: int
