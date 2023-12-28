import pytest
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from app.api.auth.token_util import JwtToken, TokenUtil, JwtTokenType, JWTError, TokenInvalidateErr

SECRET_KEY: str = "0548a115e749bd446115d6c05e95838b2f7b47568e110186e0fe81fca376e19d"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 20  # minute
REFRESH_TOKEN_EXPIRE_DAYS: int = 15  # date


class TestTokenUtil:
    user_id = "tester"
    host_id = 0

    def test_create_jwt_token_1(self):
        now = datetime.now(timezone.utc)
        token = TokenUtil.create_access_token(user_id=self.user_id)

        assert token.get_type() is JwtTokenType.ACCESS
        assert token.get_data("user_id") == self.user_id
        assert token.get_data("") is None

        compare_timestamp = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES - 1)
        assert token.is_expired(compare_timestamp=compare_timestamp.timestamp()) is False

        compare_timestamp = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES + 1)
        assert token.is_expired(compare_timestamp=compare_timestamp.timestamp()) is True

    def test_create_jwt_token_2(self):
        now = datetime.now(timezone.utc)
        token = TokenUtil.create_refresh_token(user_id=self.user_id)

        assert token.get_type() is JwtTokenType.REFRESH
        assert token.get_data("user_id") == self.user_id
        assert token.get_data("") is None

        compare_timestamp = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS - 1)
        assert token.is_expired(compare_timestamp=compare_timestamp.timestamp()) is False

        compare_timestamp = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS + 1)
        assert token.is_expired(compare_timestamp=compare_timestamp.timestamp()) is True

    def test_create_jwt_token_3(self):
        now = datetime.now(timezone.utc)
        token = TokenUtil.create_agent_token(user_id=self.user_id,
                                             host_id=self.host_id)

        assert token.get_type() is JwtTokenType.AGENT
        assert token.get_data("user_id") == self.user_id
        assert token.get_data("host_id") == self.host_id
        assert token.get_data("exp") is None
        assert token.is_expired(None) is False

    def test_create_jwt_token_4(self):
        now = datetime.now(timezone.utc)
        token = TokenUtil.create_refresh_token(user_id=self.user_id)

        other_token = TokenUtil.create_from_token(token.token_string)

        assert token.token_string == other_token.token_string

    def test_create_jwt_token_5(self):
        now = datetime.now(timezone.utc)
        token = TokenUtil.create_refresh_token(user_id=self.user_id)

        with pytest.raises(TokenInvalidateErr):
            TokenUtil.create_from_token(token.token_string[:-1])

    def test_create_make_token_1(self):
        token_info = {"data1": "data1", "data2": "data2"}
        token1 = TokenUtil.make_token(JwtTokenType.ACCESS, token_info)
        token2 = TokenUtil.make_token(JwtTokenType.ACCESS, token_info)

        assert token1.token_string == token2.token_string
        assert token1.get_type() == token2.get_type()
        assert token1.get_data("data1") == token2.get_data("data1")

        token1 = TokenUtil.make_token(JwtTokenType.REFRESH, token_info)
        token2 = TokenUtil.make_token(JwtTokenType.REFRESH, token_info)

        assert token1.token_string == token2.token_string
        assert token1.get_type() == token2.get_type()
        assert token1.get_data("data1") == token2.get_data("data1")

        token1 = TokenUtil.make_token(JwtTokenType.AGENT, token_info)
        token2 = TokenUtil.make_token(JwtTokenType.AGENT, token_info)

        assert token1.token_string == token2.token_string
        assert token1.get_type() == token2.get_type()
        assert token1.get_data("data1") == token2.get_data("data1")

    def test_create_make_token_2(self):
        token_info = {"data1": "data1", "data2": "data2"}
        token1 = TokenUtil.make_token(JwtTokenType.ACCESS, token_info)
        token2 = TokenUtil.make_token(JwtTokenType.REFRESH, token_info)

        assert token1.token_string != token2.token_string
        assert token1.get_type() != token2.get_type()
        assert token1.get_data("data1") == token2.get_data("data1")
