import pytest

from redis import RedisError

from app.api import user
from app.api.auth import service
from app.api.auth.schema import Token
from app.api.auth.token_util import JwtTokenType

from app.api.exception import api_error, crud_error
from app.api.auth.exception import TokenInvalidateErr


class TestAuthService:
    user_id = "tester"
    user_name = "user"
    user_pw = "1234567890"
    access_token = "access_token"
    refresh_token = "refresh_token"

    user_model = user.model.User(
        user_id=user_id,
        user_name=user_name,
        user_pw=user_pw,
        deleted=False)
    deleted_user_model = user.model.User(
        user_id=user_id,
        user_name=user_name,
        user_pw=user_pw,
        deleted=True)

    def test_authenticate_success(self, mocker):
        """ authenticate 성공"""
        db = mocker.MagicMock()
        # mocker.patch('app.common.passwd_util.verify_password', return_value=True)
        mocker.patch('passlib.context.CryptContext.verify', return_value=True)
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_model)

        service.authenticate(user_id=self.user_id, user_pw=self.user_pw, db=db)

    def test_authenticate_fail_1(self, mocker):
        """ authenticate 실패 db_error"""
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            service.authenticate(user_id=self.user_id, user_pw=self.user_pw, db=db)

    def test_authenticate_fail_2(self, mocker):
        """ authenticate 실패 유저가 없는 경우"""
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)

        with pytest.raises(api_error.UserNotFound):
            service.authenticate(user_id=self.user_id, user_pw=self.user_pw, db=db)

    def test_authenticate_fail_3(self, mocker):
        """ authenticate 실패, 비밀번호가 일치하지 않을 경우"""
        db = mocker.MagicMock()
        mocker.patch('passlib.context.CryptContext.verify', return_value=False)
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_model)

        with pytest.raises(api_error.Unauthorized):
            service.authenticate(user_id=self.user_id, user_pw=self.user_pw, db=db)

    def test_authenticate_fail_4(self, mocker):
        """ authenticate 실패, 삭제된 유저인 경우"""
        db = mocker.MagicMock()
        mocker.patch('passlib.context.CryptContext.verify', return_value=False)
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.deleted_user_model)

        with pytest.raises(api_error.Unauthorized):
            service.authenticate(user_id=self.user_id, user_pw=self.user_pw, db=db)

    def test_renew_token_success_1(self, mocker):
        """ token 갱신 성공"""
        redis = mocker.MagicMock()
        token_util = mocker.MagicMock()
        token_util.is_expired.return_value = False
        token_util.create.return_value = self.access_token
        token_util.token_type = JwtTokenType.REFRESH
        mocker.patch('app.api.auth.token_util.TokenUtil.from_token', return_value=token_util)

        result = service.renew_token(token=self.refresh_token, redis=redis)

        assert result == Token(access_token=self.access_token, refrest_token=None)

    def test_renew_token_success_2(self, mocker):
        """ token 갱신 성공"""
        redis = mocker.MagicMock()
        token_util = mocker.MagicMock()
        token_util.is_expired.return_value = True
        token_util.create.return_value = self.access_token
        token_util.token_type = JwtTokenType.REFRESH
        mocker.patch('app.api.auth.token_util.TokenUtil.from_token', return_value=token_util)

        result = service.renew_token(token=self.refresh_token, redis=redis)

        assert result == Token(access_token=self.access_token, refresh_token=self.access_token)

    def test_renew_token_fail_1(self, mocker):
        """ token 갱신 실패 invalidate token"""
        redis = mocker.MagicMock()
        token_util = mocker.MagicMock()
        mocker.patch('app.api.auth.token_util.TokenUtil.from_token', return_value=None) \
            .side_effect = TokenInvalidateErr

        with pytest.raises(api_error.Unauthorized):
            service.renew_token(token=self.refresh_token, redis=redis)

    def test_renew_token_fail_2(self, mocker):
        """ token 갱신 실패 Refresh-token이 아닐 경우"""
        redis = mocker.MagicMock()
        token_util = mocker.MagicMock()
        token_util.token_type = JwtTokenType.ACCESS
        mocker.patch('app.api.auth.token_util.TokenUtil.from_token', return_value=token_util)

        with pytest.raises(api_error.Unauthorized):
            service.renew_token(token=self.refresh_token, redis=redis)

    def test_renew_token_fail_3(self, mocker):
        """ token 갱신 실패 redis error"""
        redis = mocker.MagicMock()
        redis.set.side_effect = RedisError()
        token_util = mocker.MagicMock()
        token_util.is_expired.return_value = True
        token_util.create.return_value = self.access_token
        token_util.token_type = JwtTokenType.REFRESH
        mocker.patch('app.api.auth.token_util.TokenUtil.from_token', return_value=token_util)

        with pytest.raises(api_error.ServerError):
            service.renew_token(token=self.refresh_token, redis=redis)

    def test_remove_token_success(self, mocker):
        """token 삭제 성공"""
        redis = mocker.MagicMock()
        token_util = mocker.MagicMock()
        mocker.patch('app.api.auth.token_util.TokenUtil.from_token', return_value=token_util)

        service.remove_token(token=self.refresh_token, redis=redis)

    def test_remove_token_fail_1(self, mocker):
        """token 삭제 실패 invalidate token"""
        redis = mocker.MagicMock()
        token_util = mocker.MagicMock()
        mocker.patch('app.api.auth.token_util.TokenUtil.from_token', return_value=None) \
            .side_effect = TokenInvalidateErr

        with pytest.raises(api_error.Unauthorized):
            service.remove_token(token=self.refresh_token, redis=redis)

    def test_remove_token_fail_2(self, mocker):
        """token 삭제 실패 redis error"""
        redis = mocker.MagicMock()
        redis.delete.side_effect = RedisError()
        token_util = mocker.MagicMock()
        mocker.patch('app.api.auth.token_util.TokenUtil.from_token', return_value=token_util)

        with pytest.raises(api_error.ServerError):
            service.remove_token(token=self.refresh_token, redis=redis)

    def test_remove_token_fail_3(self, mocker):
        """token 삭제 실패 redis error"""
        redis = mocker.MagicMock()
        redis.setex.side_effect = RedisError()
        token_util = mocker.MagicMock()
        mocker.patch('app.api.auth.token_util.TokenUtil.from_token', return_value=token_util)

        with pytest.raises(api_error.ServerError):
            service.remove_token(token=self.refresh_token, redis=redis)
