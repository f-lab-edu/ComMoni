import pytest
from datetime import datetime, timedelta

from jose import jwt, JWTError
from app.api.auth.token_util import TokenUtil, JwtTokenType, JWTError
from app.api.auth.exception import TokenInvalidateErr

SECRET_KEY: str = "0548a115e749bd446115d6c05e95838b2f7b47568e110186e0fe81fca376e19d"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 20  # minute
REFRESH_TOKEN_EXPIRE_MINUTES: int = 15  # date


class TestTokenUtil:
    user_id = "tester"
    host_id = 0
    expire = datetime.utcnow()

    def test_create_success_1(self):
        """
        token 생성 및 디코드 성공
        """
        token_util = TokenUtil(
            user_id=self.user_id,
            host_id=self.host_id,
            expire=int(self.expire.timestamp())
        )
        token = token_util.create(JwtTokenType.ACCESS)

        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    def test_create_success_2(self):
        """
        token 생성 및 TokenUtil 객체 생성 성공
        """
        token_util = TokenUtil(
            user_id=self.user_id,
            host_id=self.host_id,
            expire=self.expire
        )
        token = token_util.create(JwtTokenType.ACCESS)

        TokenUtil.from_token(token)

    def test_create_fail_1(self):
        token_util = TokenUtil(
            user_id=self.user_id,
            host_id=self.host_id,
            expire=int(self.expire.timestamp())
        )
        token = token_util.create(JwtTokenType.ACCESS)

        token = token[:-1]

        with pytest.raises(JWTError):
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    def test_create_fail_2(self):
        token_util = TokenUtil(
            user_id=self.user_id,
            host_id=self.host_id,
            expire=int(self.expire.timestamp())
        )
        token = token_util.create(JwtTokenType.ACCESS)

        token = token[:-1]

        with pytest.raises(TokenInvalidateErr):
            TokenUtil.from_token(token)

    def test_expire_check_success_1(self):
        """
        token 생성 및 TokenUtil 만료일자 체크
        """
        token_util = TokenUtil(
            user_id=self.user_id,
            host_id=self.host_id,
            expire=int(self.expire.timestamp())
        )
        token = token_util.create(JwtTokenType.ACCESS)

        new_token_util = TokenUtil.from_token(token)
        compare_time_delta = self.expire + timedelta(days=-2)

        assert new_token_util.is_expired(compare_time_delta.timestamp()) == False

    def test_expire_check_success_2(self):
        """
        token 생성 및 TokenUtil 만료일자 체크
        """
        token_util = TokenUtil(
            user_id=self.user_id,
            host_id=self.host_id,
            expire=int(self.expire.timestamp())
        )
        token = token_util.create(JwtTokenType.ACCESS)

        new_token_util = TokenUtil.from_token(token)
        compare_time_delta = self.expire + timedelta(days=2)

        assert new_token_util.is_expired(compare_time_delta.timestamp()) == True

    def test_expire_check_success_3(self):
        """
        token 생성 및 TokenUtil 만료일자 체크
        """
        token_util = TokenUtil(
            user_id=self.user_id,
            host_id=self.host_id,
            expire=int(self.expire.timestamp())
        )
        token = token_util.create(JwtTokenType.REFRESH)

        new_token_util = TokenUtil.from_token(token)
        compare_time_delta = self.expire + timedelta(days=16)

        assert new_token_util.is_expired(compare_time_delta.timestamp()) == True

    def test_expire_check_success_4(self):
        """
        token 생성 및 TokenUtil 만료일자 체크
        """
        token_util = TokenUtil(
            user_id=self.user_id,
            host_id=self.host_id,
            expire=int(self.expire.timestamp())
        )
        token = token_util.create(JwtTokenType.REFRESH)

        new_token_util = TokenUtil.from_token(token)
        compare_time_delta = self.expire + timedelta(days=13)

        assert new_token_util.is_expired(compare_time_delta.timestamp()) == False
