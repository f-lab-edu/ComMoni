from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.common.redis_util import get_redis, RedisUtil, RedisUtilError

from app.api import user, commanage
from app.api.auth.schema import Token, TokenSet
from app.api.auth.token_util import TokenUtil, JwtToken, JwtTokenType
from app.common.passwd_util import PasswdUtil

from app.api.exception import api_error, crud_error
from app.api.auth.token_util import TokenInvalidateErr

from app.configs.log import logger
from app.configs.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)

KEY_REFRESH = "refresh_token"
KEY_AGENT = "agent_token"
KEY_LOGOUT = "logout"
KEY_USER_ID = "user_id"
KEY_HOST_ID = "host_id"


class AuthService:

    def __init__(self, db: Session = None, redis: RedisUtil = None):
        self.db = db
        self.redis = redis

    @staticmethod
    def make_refresh_key_name(user_id: str) -> str:
        """redis에서 사용할 refresh token key 이름 생성"""
        return f"{user_id}.{KEY_REFRESH}"

    @staticmethod
    def make_agent_key_name(user_id: str, host_id: int) -> str:
        """redis에서 사용할 agent token key 이름 생성"""
        return f"{user_id}.{KEY_AGENT}.{host_id}"

    @staticmethod
    def make_logout_key_name(user_id: str) -> str:
        """redis에서 사용할 logout acces token key 이름 생성"""
        return f"{user_id}.{KEY_LOGOUT}"

    def get_user(self, user_id: str) -> user.model.User:
        """User 상태를 확인 후, 정상적인 User만 반환"""
        try:
            check_user = user.crud.UserCRUD(self.db).get(
                user.schema.UserGet(user_id=user_id)
            )
        except crud_error.DatabaseGetErr:
            logger.error(f"[auth-service] UserCRUD get error")
            raise api_error.ServerError(f"[auth-service] UserCRUD error")

        if not check_user:
            logger.error(f"[auth-service] user[{user_id} is not found")
            raise api_error.UserNotFound(user_id=user_id)

        if check_user.deleted:
            logger.error(f"[auth-service] user[{user_id}] is deleted user")
            raise api_error.Unauthorized(message="already deleted user")

        return check_user

    def authenticate(self, user_id: str, user_pw: str):
        """
        로그인 정보로 사용자 인증
        :param user_id: 사용자 아이디
        :param user_pw: 사용자 비밀번호
        :return: AuthService(self)
        """
        check_user = self.get_user(user_id=user_id)

        if not PasswdUtil.verify(plain=user_pw, hashed=check_user.user_pw):
            logger.error(f"[auth-service] user password is invalid")
            raise api_error.Unauthorized("password is invalid")

        logger.info(f"[auth-service] authenticate success. id : {user_id}")
        return self

    def authenticate_host(self, host_id: int) -> None:
        """
        host_id 인증
        :param host_id: Commanage에 등록된 hoat_id
        :return: None
        """
        try:
            result = commanage.crud.CommanageCRUD(self.db).get(
                commanage.schema.ComManageByHost(host_id=host_id)
            )
        except crud_error.DatabaseGetErr:
            logger.error(f"[auth-service] CommanageCRUD get error")
            raise api_error.ServerError(f"[auth-service] CommanageCRUD error")

        if not result:
            logger.error(f"[auth-service] host[{host_id}] is not found")
            raise api_error.CommanageNotFound(host_id=host_id)

    def create_access_token(self, user_id: str) -> Token:
        """access token 생성"""
        access_token = TokenUtil.create_access_token(user_id=user_id)
        return Token(value=access_token.token_string, type=JwtTokenType.ACCESS)

    def create_refresh_token(self, user_id: str) -> Token:
        """refresh token 생성"""
        refresh_token = TokenUtil.create_refresh_token(user_id=user_id)

        try:
            key = self.make_refresh_key_name(user_id=user_id)
            self.redis.set(key=key, value=refresh_token.token_string)
        except RedisUtilError as err:
            logger.error(f"[auth-service] redis error : {err}")
            raise api_error.ServerError(f"[auth-service] redis error")

        return Token(value=refresh_token.token_string, type=JwtTokenType.REFRESH)

    def create_agent_token(self, user_id: str, host_id: int) -> Token:
        """agent token 생성"""
        agent_token = TokenUtil.create_agent_token(user_id=user_id, host_id=host_id)

        try:
            key = self.make_agent_key_name(user_id=user_id, host_id=host_id)
            self.redis.set(key=key, value=agent_token.token_string)
        except RedisUtilError as err:
            logger.error(f"[auth-service] redis error : {err}")
            raise api_error.ServerError(f"[auth-service] redis error")

        return Token(value=agent_token.token_string, type=JwtTokenType.AGENT)

    def create_token_set(self, user_id: str, temp_login: bool = False) -> TokenSet:
        """access/refresh token을 같이 생성"""
        access_token = self.create_access_token(user_id=user_id)
        if not temp_login:
            refresh_token = self.create_refresh_token(user_id=user_id)
            return TokenSet(access_token=access_token.value, refresh_token=refresh_token.value)

        return TokenSet(access_token=access_token.value, refresh_token="")

    def renew_token(self, token: JwtToken) -> TokenSet:
        """토큰 갱신"""
        if token.get_type() != JwtTokenType.REFRESH:
            raise api_error.Unauthorized("not support token type")

        user_id = token.get_data(KEY_USER_ID)
        refresh_token = None
        compare_datetime = datetime.utcnow() + timedelta(days=settings.DATE_BEFORE_EXPIRATION)

        if token.is_expired(int(compare_datetime.timestamp())):
            logger.info("[auth-service] refresh token's expiration date is approaching. Renew the token")
            refresh_token = self.create_refresh_token(user_id=user_id)

        access_token = self.create_access_token(user_id=user_id)
        if refresh_token is None:
            return TokenSet(access_token=access_token.value, refresh_token="")

        return TokenSet(access_token=access_token.value, refresh_token=refresh_token.value)

    def remove_token(self, token: JwtToken) -> None:
        """토큰 삭제"""
        if token.get_type() != JwtTokenType.ACCESS:
            raise api_error.Unauthorized("not support token type")

        user_id = token.get_data(KEY_USER_ID)
        expire_minutes = 60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES

        try:
            delete_key = self.make_refresh_key_name(user_id=user_id)
            self.redis.delete(delete_key)
            self.redis.set_with_expire(
                key=self.make_logout_key_name(user_id=user_id),
                value=token.get_token(),
                expire_minutes=expire_minutes
            )
        except RedisUtilError as err:
            logger.error(f"[auth-service] redis error : {err}")
            raise api_error.ServerError(f"[auth-service] redis error")

    def verify_access_token(self, token: JwtToken):
        """access token 인증"""
        if token.get_type() != JwtTokenType.ACCESS:
            raise api_error.Unauthorized("not support token type")

        user_id = token.get_data(KEY_USER_ID)
        self.get_user(user_id=user_id)

    def verify_refresh_token(self, token: JwtToken):
        """refresh token 인증"""
        if token.get_type() != JwtTokenType.REFRESH:
            raise api_error.Unauthorized("not support token type")

        user_id = token.get_data(KEY_USER_ID)
        self.get_user(user_id=user_id)

        try:
            key = self.make_refresh_key_name(user_id=user_id)
            result = self.redis.get(key=key)
        except RedisUtilError as err:
            logger.error(f"[auth-service] redis error : {err}")
            raise api_error.ServerError(f"[auth-service] redis error")

        if result is None:
            raise api_error.Unauthorized("Not a registered token")

    def verify_agent_token(self, token: JwtToken):
        """agent token 인증"""
        if token.get_type() != JwtTokenType.AGENT:
            raise api_error.Unauthorized("not support token type")

        host_id = int(token.get_data(key=KEY_HOST_ID))
        self.authenticate_host(host_id=host_id)

        user_id = token.get_data(key=KEY_USER_ID)
        key = self.make_agent_key_name(user_id=user_id, host_id=host_id)

        try:
            result = self.redis.get(key=key)
        except RedisUtilError as err:
            logger.error(f"[auth-service] redis error : {err}")
            raise api_error.ServerError(f"[auth-service] redis error")

        if result is None:
            raise api_error.Unauthorized("Not a registered token")


def get_auth_service(db: Session = Depends(get_db),
                     redis: RedisUtil = Depends(get_redis)):
    """auth service 의존성"""
    yield AuthService(db=db, redis=redis)


def get_jwt_token(token: str = Depends(oauth2_scheme)):
    """JwtToken 의존성"""
    try:
        yield TokenUtil.create_from_token(token)
    except TokenInvalidateErr as err:
        raise api_error.Unauthorized(message=str(err))


def verify_agent_token(token: JwtToken = Depends(get_jwt_token),
                       auth_service: AuthService = Depends(get_auth_service)):
    """agent token 인증 의존성"""
    auth_service.verify_agent_token(token)


def verify_access_token(token: JwtToken = Depends(get_jwt_token),
                        auth_service: AuthService = Depends(get_auth_service)):
    """access token 인증 의존성"""
    auth_service.verify_access_token(token)
