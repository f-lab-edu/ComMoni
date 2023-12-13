from enum import Enum
from datetime import datetime, timedelta

from jose import jwt, JWTError
from app.api.auth import exception

from app.configs.config import settings


class JwtTokenType(Enum):
    """
    token 타입 정의를 위한 enum class
    """
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"

    def __str__(self):
        return str(self.value)


class TokenUtil:
    """
    token 관련 유틸 클래스
    """

    def __init__(self, user_id: str, host_id: int, token_type: JwtTokenType = None, expire: int = 0):
        self.user_id = user_id
        self.host_id = host_id
        self.expire = expire
        self.token_type = token_type

    def create(self, token_type: JwtTokenType) -> str:
        """
        token 생성
        :param token_type: 토큰 타입
        :return: str
        """
        if token_type == JwtTokenType.ACCESS:
            add_expire_timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            add_expire_timedelta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        self.expire = datetime.utcnow() + add_expire_timedelta
        to_encode = {
            "exp": self.expire,
            "user_id": str(self.user_id),
            "host_id": self.host_id,
            "type": str(token_type),
        }
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def is_expired(self, compare_timestamp: int):
        return self.expire < compare_timestamp

    @classmethod
    def from_token(cls, token: str):
        """
        token에서 TokenUtil 클래스 생성 클래스 메서드
        :param token: 변환하려는 token
        :return: TokenUtil
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("user_id")
            host_id = payload.get("host_id")
            expire = payload.get("exp")

            if payload.get("type") == str(JwtTokenType.ACCESS):
                token_type = JwtTokenType.ACCESS
            else:
                token_type = JwtTokenType.REFRESH

            return cls(user_id=user_id, host_id=host_id, expire=expire, token_type=token_type)
        except JWTError as err:
            raise exception.TokenInvalidateErr(err)
