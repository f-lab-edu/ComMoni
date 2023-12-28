from enum import Enum
from datetime import datetime, timedelta

from jose import jwt, JWTError

from app.configs.config import settings


class JwtTokenType(Enum):
    """
    token 타입 정의를 위한 enum class
    """
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"
    AGENT = "AGENT"

    def __str__(self):
        """token 스트링 변환 매직메서드"""
        return str(self.value)


class TokenInvalidateErr(Exception):
    pass


class JwtToken:
    """JWT 토큰 클래스"""

    def __init__(self, token: str):
        """토큰 생성자"""
        try:
            self.payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError as err:
            raise TokenInvalidateErr(err)

        self.token_string = token

    def is_expired(self, compare_timestamp: int) -> bool:
        """
        토큰의 만료일자를 파라미터와 비교하여 만료상태 확인
        Agent Token은 만료일자가 없음으로 항상 False 반환
        :param compare_timestamp: 비교할 기준 시간(datetime의 timestamp값)
        :return: bool
        """
        if self.get_type() == JwtTokenType.AGENT:
            return False

        expire = int(self.payload['exp'])
        return expire < compare_timestamp

    def get_token(self) -> str:
        """
        토큰 원본 반환
        :return: str
        """
        return self.token_string

    def get_type(self) -> JwtTokenType:
        """
        토큰 타입 확인
        :return: JwtTokenType
        """
        return JwtTokenType(self.payload['type'])

    def get_data(self, key: str) -> str:
        """
        토큰의 만료일자를 제외한 데이터 가져오기.
        :param key: 찾으려는 데이터 키
        :return: str
        """
        return self.payload.get(key)


class TokenUtil:
    @classmethod
    def create_from_token(cls, token: str):
        """
        토큰에서 JwtToken객체 생성
        :param token: 문자열로 된 토큰
        :return: JwtToken
        """
        return JwtToken(token)

    @classmethod
    def create_access_token(cls, user_id: str):
        """
        Access Type의 토큰 생성
        :param user_id: 사용자 아이디
        :return: JwtToken
        """
        return cls.make_token(
            token_type=JwtTokenType.ACCESS,
            token_info={"user_id": user_id}
        )

    @classmethod
    def create_refresh_token(cls, user_id: str):
        """
        Refresh Type의 토큰 생성
        :param user_id: 사용자 아이디
        :return: JwtToken
        """
        return cls.make_token(
            token_type=JwtTokenType.REFRESH,
            token_info={"user_id": user_id}
        )

    @classmethod
    def create_agent_token(cls, user_id: str, host_id: int):
        """
        Agent Type의 토큰 생성
        :param user_id: 사용자 아이디
        :param host_id: 호스트 아이디(commanage)
        :return: JwtToken
        """
        return cls.make_token(
            token_type=JwtTokenType.AGENT,
            token_info={"user_id": user_id, "host_id": host_id}
        )

    @classmethod
    def make_token(cls, token_type: JwtTokenType, token_info: dict):
        """
        토큰 생성
        :param token_type: 생성할 토큰 타입
        :param token_info: 토큰에 추가할 데이터
        :return: JwtToken
        """
        expire = cls.make_expire(token_type)
        to_encode = {**expire, **token_info}

        try:
            token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        except JWTError as err:
            raise TokenInvalidateErr(err)

        return JwtToken(token)

    @classmethod
    def make_expire(cls, token_type: JwtTokenType):
        """
        토큰의 type을 기준으로 만료일자 생성
        :param token_type: 토큰 타입
        :return: dict
        """
        if token_type == JwtTokenType.ACCESS:
            return {
                'exp': datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                "type": str(JwtTokenType.ACCESS)
            }
        elif token_type == JwtTokenType.REFRESH:
            return {
                'exp': datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
                "type": str(JwtTokenType.REFRESH)
            }
        else:
            return {"type": str(JwtTokenType.AGENT)}
