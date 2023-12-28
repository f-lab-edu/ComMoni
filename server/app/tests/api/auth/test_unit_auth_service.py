import pytest

import app.api.auth.service
from app.api.auth.service import AuthService
from app.api.auth.service import KEY_USER_ID, KEY_LOGOUT, KEY_HOST_ID
from app.api.auth.service import KEY_AGENT, KEY_REFRESH
from app.api.auth.token_util import JwtTokenType

from app.api.user.model import User
from app.api.commanage.model import ComManage

from app.api.exception import api_error, crud_error
from app.common.redis_util import RedisUtilError


class TestAuthService:
    user_id = "tester"
    host_id = 1
    user_name = "user"
    user_pw = "1234567890"
    access_token = "access_token"
    refresh_token = "refresh_token"

    user_model = User(
        user_id=user_id,
        user_pw=user_pw,
        user_name=user_name,
        deleted=False,
    )

    deleted_user_model = User(
        user_id=user_id,
        user_pw=user_pw,
        user_name=user_name,
        deleted=True,
    )

    def test_make_refresh_key_name(self):
        """refresh_key 생성 테스트"""
        key = AuthService.make_refresh_key_name(user_id=self.user_id)
        assert key == f"{self.user_id}.{KEY_REFRESH}"

    def test_make_agent_key_name(self):
        """agent_key 생성 테스트"""
        key = AuthService.make_agent_key_name(user_id=self.user_id, host_id=self.host_id)
        assert key == f"{self.user_id}.{KEY_AGENT}.{self.host_id}"

    def test_make_logout_key_name(self):
        """logout_key 생성 테스트"""
        key = AuthService.make_logout_key_name(user_id=self.user_id)
        assert key == f"{self.user_id}.{KEY_LOGOUT}"

    def test_get_user_1(self, mocker):
        """AuthService get_user 테스트 정상"""
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_model)

        result = AuthService(db=db).get_user(user_id=self.user_id)

        assert result == self.user_model

    def test_get_user_2(self, mocker):
        """AuthService get_user 테스트 DB에러 발생"""
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr()

        with pytest.raises(api_error.ServerError):
            AuthService(db=db).get_user(user_id=self.user_id)

    def test_get_user_3(self, mocker):
        """AuthService get_user 유저가 없을 경우"""
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)

        with pytest.raises(api_error.UserNotFound):
            AuthService(db=db).get_user(user_id=self.user_id)

    def test_get_user_4(self, mocker):
        """AuthService get_user 유저가 삭제되었을 경우"""
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.deleted_user_model)

        with pytest.raises(api_error.Unauthorized):
            AuthService(db=db).get_user(self.user_id)

    def test_authenticate_1(self, mocker):
        """AuthService authenticate 성공"""
        mocker.patch('app.api.auth.service.AuthService.get_user', return_value=self.user_model)
        mocker.patch('app.common.passwd_util.PasswdUtil.verify', return_value=True)

        AuthService().authenticate(user_id=self.user_id, user_pw=self.user_pw)

    def test_authenticate_2(self, mocker):
        """AuthService authenticate. PasswdUtil.verify 가 틀릴경우"""
        mocker.patch('app.api.auth.service.AuthService.get_user', return_value=self.user_model)
        mocker.patch('app.common.passwd_util.PasswdUtil.verify', return_value=False)

        with pytest.raises(api_error.Unauthorized):
            AuthService().authenticate(user_id=self.user_id, user_pw=self.user_pw)

    def test_authenticate_host_1(self, mocker):
        """AuthService authenticate_host 테스트 성공"""
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=ComManage())

        AuthService().authenticate_host(host_id=self.host_id)

    def test_authenticate_host_2(self, mocker):
        """AuthService authenticate_host 테스트 DB 에러 발생"""
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr()

        with pytest.raises(api_error.ServerError):
            AuthService().authenticate_host(host_id=self.host_id)

    def test_authenticate_host_3(self, mocker):
        """AuthService authenticate_host return 이 None일 때"""
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=None)

        with pytest.raises(api_error.CommanageNotFound):
            AuthService().authenticate_host(host_id=self.host_id)

    def test_create_access_token(self):
        """AuthService access_token 생성 테스트"""
        token = AuthService().create_access_token(user_id=self.user_id)
        assert token.type == JwtTokenType.ACCESS

    def test_refresh_access_token_1(self, mocker):
        """AuthService refresh_token 생성 테스트"""
        redis = mocker.Mock()
        result_token = mocker.Mock()
        result_token.token_string = "token"
        mocker.patch('app.api.auth.token_util.TokenUtil.create_refresh_token',
                     return_value=result_token)

        token = AuthService(redis=redis).create_refresh_token(user_id=self.user_id)
        assert token.type == JwtTokenType.REFRESH

    def test_refresh_access_token_2(self, mocker):
        """AuthService refresh_token 생성 redis 에러"""
        redis = mocker.Mock()
        redis.set.side_effect = RedisUtilError()
        result_token = mocker.Mock()
        result_token.token_string = "token"
        mocker.patch('app.api.auth.token_util.TokenUtil.create_refresh_token',
                     return_value=result_token)

        with pytest.raises(api_error.ServerError):
            AuthService(redis=redis).create_refresh_token(user_id=self.user_id)

    def test_agent_access_token_1(self, mocker):
        """AuthService agent_token 생성 테스트"""
        redis = mocker.Mock()
        result_token = mocker.Mock()
        result_token.token_string = "token"
        mocker.patch('app.api.auth.token_util.TokenUtil.create_agent_token',
                     return_value=result_token)

        token = AuthService(redis=redis).create_agent_token(user_id=self.user_id,
                                                            host_id=self.host_id)
        assert token.type == JwtTokenType.AGENT

    def test_agent_access_token_2(self, mocker):
        """AuthService agent_token 생성 redis 에러"""
        redis = mocker.Mock()
        redis.set.side_effect = RedisUtilError()
        result_token = mocker.Mock()
        result_token.token_string = "token"
        mocker.patch('app.api.auth.token_util.TokenUtil.create_agent_token',
                     return_value=result_token)

        with pytest.raises(api_error.ServerError):
            AuthService(redis=redis).create_agent_token(user_id=self.user_id,
                                                        host_id=self.host_id)

    def test_create_token_set_1(self, mocker):
        """AuthService agent,refresh token 생성"""
        access_token = mocker.Mock()
        access_token.value = "access"
        mocker.patch("app.api.auth.service.AuthService.create_access_token",
                     return_value=access_token)
        refresh_token = mocker.Mock()
        refresh_token.value = "refresh"
        mocker.patch("app.api.auth.service.AuthService.create_refresh_token",
                     return_value=refresh_token)

        token_set = AuthService().create_token_set(user_id=self.user_id)

        assert token_set.access_token == access_token.value
        assert token_set.refresh_token == refresh_token.value

    def test_create_token_set_2(self, mocker):
        """AuthService agent,refresh token 생성, temp_login"""
        access_token = mocker.Mock()
        access_token.value = "access"
        mocker.patch("app.api.auth.service.AuthService.create_access_token",
                     return_value=access_token)

        token_set = AuthService().create_token_set(user_id=self.user_id, temp_login=True)

        assert token_set.access_token == access_token.value
        assert token_set.refresh_token == ""

    def test_renew_token_1(self, mocker):
        """AuthService token 갱신 성공"""
        access_token = mocker.Mock()
        access_token.value = "access"
        mocker.patch("app.api.auth.service.AuthService.create_access_token",
                     return_value=access_token)
        refresh_token = mocker.Mock()
        refresh_token.value = "refresh"
        mocker.patch("app.api.auth.service.AuthService.create_refresh_token",
                     return_value=refresh_token)

        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.REFRESH
        token.get_data.return_value = "user_id"
        token.is_expired.return_value = True

        token_set = AuthService().renew_token(token=token)
        assert token_set.access_token == access_token.value
        assert token_set.refresh_token == refresh_token.value

    def test_renew_token_2(self, mocker):
        """AuthService token 갱신 실패, 토큰 타입 불일치"""
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.AGENT

        with pytest.raises(api_error.Unauthorized):
            AuthService().renew_token(token=token)

    def test_renew_token_3(self, mocker):
        """AuthService token 갱신, access_token만 갱신"""
        access_token = mocker.Mock()
        access_token.value = "access"
        mocker.patch("app.api.auth.service.AuthService.create_access_token",
                     return_value=access_token)
        refresh_token = mocker.Mock()
        refresh_token.value = "refresh"
        mocker.patch("app.api.auth.service.AuthService.create_refresh_token",
                     return_value=refresh_token)

        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.REFRESH
        token.get_data.return_value = "user_id"
        token.is_expired.return_value = False

        token_set = AuthService().renew_token(token=token)
        assert token_set.access_token == access_token.value
        assert token_set.refresh_token == ""

    def test_remove_token_1(self, mocker):
        """AuthService 토큰 삭제"""
        redis = mocker.Mock()
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.ACCESS
        mocker.patch("app.api.auth.service.AuthService.make_refresh_key_name",
                     return_value="delete_key")

        AuthService(redis=redis).remove_token(token=token)

    def test_remove_token_2(self, mocker):
        """AuthService 토큰 삭제 실패, 토큰 타입 불일치"""
        redis = mocker.Mock()
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.REFRESH

        with pytest.raises(api_error.Unauthorized):
            AuthService(redis=redis).remove_token(token=token)

    def test_remove_token_3(self, mocker):
        """AuthService 토큰 삭제 실패, redis error"""
        redis = mocker.Mock()
        redis.delete.side_effect = RedisUtilError()
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.ACCESS
        mocker.patch("app.api.auth.service.AuthService.make_refresh_key_name",
                     return_value="delete_key")

        with pytest.raises(api_error.ServerError):
            AuthService(redis=redis).remove_token(token=token)

    def test_verify_access_token_1(self, mocker):
        """AuthService access_token 확인"""
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.ACCESS
        token.get_data.return_value = "data"
        mocker.patch("app.api.auth.service.AuthService.get_user",
                     return_value=True)

        AuthService().verify_access_token(token=token)

    def test_verify_access_token_2(self, mocker):
        """AuthService access_token 토큰 타입 불일치"""
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.REFRESH
        token.get_data.return_value = "data"
        mocker.patch("app.api.auth.service.AuthService.get_user",
                     return_value=True)

        with pytest.raises(api_error.Unauthorized):
            AuthService().verify_access_token(token=token)

    def test_verify_refresh_token_1(self, mocker):
        """AuthService refresh_token 확인"""
        redis = mocker.Mock()
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.REFRESH
        token.get_data.return_value = "data"
        mocker.patch("app.api.auth.service.AuthService.get_user",
                     return_value=True)
        mocker.patch("app.api.auth.service.AuthService.make_refresh_key_name",
                     return_value="delete_key")

        AuthService(redis=redis).verify_refresh_token(token=token)

    def test_verify_refresh_token_2(self, mocker):
        """AuthService refresh_token 토큰 타입 불일치"""
        redis = mocker.Mock()
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.AGENT
        token.get_data.return_value = "data"
        mocker.patch("app.api.auth.service.AuthService.get_user",
                     return_value=True)
        mocker.patch("app.api.auth.service.AuthService.make_refresh_key_name",
                     return_value="delete_key")

        with pytest.raises(api_error.Unauthorized):
            AuthService(redis=redis).verify_refresh_token(token=token)

    def test_verify_refresh_token_3(self, mocker):
        """AuthService refresh_token redis error"""
        redis = mocker.Mock()
        redis.get.side_effect = RedisUtilError
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.REFRESH
        token.get_data.return_value = "data"
        mocker.patch("app.api.auth.service.AuthService.get_user",
                     return_value=True)
        mocker.patch("app.api.auth.service.AuthService.make_refresh_key_name",
                     return_value="delete_key")

        with pytest.raises(api_error.ServerError):
            AuthService(redis=redis).verify_refresh_token(token=token)

    def test_verify_refresh_token_4(self, mocker):
        """AuthService refresh_token token이 redis에 없을 때"""
        redis = mocker.Mock()
        redis.get.return_value = None
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.AGENT
        token.get_data.return_value = "data"
        mocker.patch("app.api.auth.service.AuthService.get_user",
                     return_value=True)
        mocker.patch("app.api.auth.service.AuthService.make_refresh_key_name",
                     return_value="delete_key")

        with pytest.raises(api_error.Unauthorized):
            AuthService(redis=redis).verify_refresh_token(token=token)

    def test_verify_agent_token_1(self, mocker):
        """AuthService agent_token 확인"""
        redis = mocker.Mock()
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.AGENT
        token.get_data.return_value = "1"
        mocker.patch("app.api.auth.service.AuthService.get_user",
                     return_value=True)
        mocker.patch("app.api.auth.service.AuthService.make_agent_key_name",
                     return_value="delete_key")
        mocker.patch("app.api.auth.service.AuthService.authenticate_host",
                     return_value=True)

        AuthService(redis=redis).verify_agent_token(token=token)

    def test_verify_agent_token_2(self, mocker):
        """AuthService agent_token 토큰 타입 불일치"""
        redis = mocker.Mock()
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.REFRESH
        token.get_data.return_value = "1"
        mocker.patch("app.api.auth.service.AuthService.get_user",
                     return_value=True)
        mocker.patch("app.api.auth.service.AuthService.make_agent_key_name",
                     return_value="delete_key")
        mocker.patch("app.api.auth.service.AuthService.authenticate_host",
                     return_value=True)

        with pytest.raises(api_error.Unauthorized):
            AuthService(redis=redis).verify_agent_token(token=token)

    def test_verify_agent_token_3(self, mocker):
        """AuthService agent_token redis error"""
        redis = mocker.Mock()
        redis.get.side_effect = RedisUtilError
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.AGENT
        token.get_data.return_value = "1"
        mocker.patch("app.api.auth.service.AuthService.get_user",
                     return_value=True)
        mocker.patch("app.api.auth.service.AuthService.make_agent_key_name",
                     return_value="delete_key")
        mocker.patch("app.api.auth.service.AuthService.authenticate_host",
                     return_value=True)

        with pytest.raises(api_error.ServerError):
            AuthService(redis=redis).verify_agent_token(token=token)

    def test_verify_agent_token_4(self, mocker):
        """AuthService agent_token token이 redis에 없을 때"""
        redis = mocker.Mock()
        redis.get.return_value = None
        token = mocker.Mock()
        token.get_type.return_value = JwtTokenType.AGENT
        token.get_data.return_value = "1"
        mocker.patch("app.api.auth.service.AuthService.get_user",
                     return_value=True)
        mocker.patch("app.api.auth.service.AuthService.make_agent_key_name",
                     return_value="delete_key")
        mocker.patch("app.api.auth.service.AuthService.authenticate_host",
                     return_value=True)

        with pytest.raises(api_error.Unauthorized):
            AuthService(redis=redis).verify_agent_token(token=token)
