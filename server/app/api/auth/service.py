from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from redis import Redis
from redis.exceptions import RedisError

from app.database import get_db
from app.common.redis_util import get_redis
from app.api import user, commanage
from app.api.auth.schema import Token
from app.api.auth.token_util import TokenUtil, JwtTokenType
from app.common.passwd_util import verify_password

from app.api.auth.exception import TokenInvalidateErr
from app.api.exception import api_error

from app.configs.log import logger
from app.configs.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


def authenticate(user_id: str, user_pw: str, db: Session) -> None:
    """
    아이디와 비밀번호로 인증
    :param user_id: 사용자 아이디
    :param user_pw: 사죶아 비밀번호
    :param db: db session
    :return: None
    """
    try:
        get_user = user.crud.UserCRUD(db).get(
            user.schema.UserGet(user_id=user_id)
        )
    except user.exception.DatabaseGetErr:
        logger.error(f"[auth-service] UserCRUD get error")
        raise api_error.ServerError(f"[auth-service] UserCRUD error")

    if not get_user:
        logger.error(f"[auth-service] user[{user_id} is not found")
        raise api_error.UserNotFound(user_id=user_id)

    if not verify_password(plain_password=user_pw, hashed_password=get_user.user_pw):
        logger.error(f"[auth-service] user password is invalid")
        raise api_error.Unauthorized()

    if get_user.deleted:
        logger.error(f"[auth-service] user[{user_id}] is deleted user")
        raise api_error.Unauthorized()

    logger.info(f"[auth-service] authenticate success. {user_id}")


def create_token(db: Session, redis: Redis, user_id: str, host_id: int = 0) -> Token:
    """
    token 생성
    :param db: db session
    :param redis: redis session
    :param user_id: 사용자 아이디
    :param host_id: 호스트 아이디
    :return: Token 스키마
    """
    if host_id != 0:
        # host id 가 있을경우 commanage용 토큰 생성
        try:
            result = commanage.crud.CommanageCRUD(db).get(
                commanage.schema.ComManageByHost(host_id=host_id)
            )
        except commanage.exception.DatabaseGetErr:
            logger.error(f"[auth-service] CommanageCRUD get error")
            raise api_error.ServerError(f"[auth-service] CommanageCRUD error")

        if not result:
            logger.error(f"[auth-service] host[{host_id}] is not found")
            raise api_error.CommanageNotFound(host_id=host_id)

    token_util = TokenUtil(user_id=user_id, host_id=host_id)
    access_token = token_util.create(token_type=JwtTokenType.ACCESS)
    refresh_token = token_util.create(token_type=JwtTokenType.REFRESH)

    # refresh 저장
    try:
        redis.set(name=user_id, value=refresh_token)
    except RedisError as err:
        logger.error(f"[auth-service] redis error : {err}")
        raise api_error.ServerError(f"[auth-service] redis error")

    return Token(access_token=access_token, refresh_token=refresh_token)


def renew_token(token: str, redis: Redis) -> Token:
    """
    token 갱신
    :param token: 토큰(리프레시 토큰)
    :param redis: redis session
    :return: Token 스키마
    """
    try:
        token_util = TokenUtil.from_token(token)
    except TokenInvalidateErr as err:
        logger.error(f"[auth-service] TokenUtil error : {err}")
        raise api_error.Unauthorized()

    if token_util.token_type != JwtTokenType.REFRESH:
        logger.error(f"[auth-service] current Token is not Refresh-token")
        raise api_error.Unauthorized()

    # refresh token 만료전 체크일자
    compare_timedelta = (datetime.utcnow() + timedelta(days=settings.DATE_BEFORE_EXPIRATION)).timestamp()
    if token_util.is_expired(compare_timedelta):
        logger.info("[auth-service] refresh token's expiration date is approaching. Renew the token")
        refresh_token = token_util.create(token_type=JwtTokenType.REFRESH)

        try:
            redis.set(name=token_util.user_id, value=refresh_token)
        except RedisError as err:
            logger.error(f"[auth-service] redis error : {err}")
            raise api_error.ServerError(f"[auth-service] redis error")
    else:
        refresh_token = None

    access_token = token_util.create(token_type=JwtTokenType.ACCESS)
    return Token(access_token=access_token, refresh_token=refresh_token)


def remove_token(token: str, redis: Redis) -> None:
    """
    token 제거
    :param token: 제거할 토큰
    :param redis: redis session
    :return: None
    """
    try:
        token_util = TokenUtil.from_token(token)
    except TokenInvalidateErr as err:
        logger.error(f"[auth-service] TokenUtil error : {err}")
        raise api_error.Unauthorized()

    expire_time = 60 * settings.ACCESS_TOKEN_EXPIRE_MINUTES

    try:
        redis.delete(token_util.user_id)
        redis.setex(name=f"{token_util.user_id}_logout",
                    value=token,
                    time=expire_time)
    except RedisError as err:
        logger.error(f"[auth-service] redis error : {err}")
        raise api_error.ServerError(f"[auth-service] redis error")


def verify_token(db: Session = Depends(get_db),
                 redis: Redis = Depends(get_redis),
                 token: str = Depends(oauth2_scheme)):
    """
    token 인증
    :param db: db session
    :param redis: redis session
    :param token: 인증할 token
    :return:
    """
    try:
        token_util = TokenUtil.from_token(token)
    except TokenInvalidateErr as err:
        logger.error(f"[auth-service] TokenUtil error : {err}")
        raise api_error.Unauthorized()

    try:
        get_user = user.crud.UserCRUD(db).get(
            user.schema.UserGet(user_id=token_util.user_id)
        )
    except user.exception.DatabaseGetErr:
        logger.error(f"[auth-service] UserCRUD get error")
        raise api_error.ServerError(f"[auth-service] UserCRUD error")

    if not get_user:
        logger.error(f"[auth-service] user[{token_util.user_id} is not found")
        raise api_error.UserNotFound(user_id=token_util.user_id)

    if get_user.deleted:
        logger.error(f"[auth-service] user[{token_util.user_id} is deleted user")
        raise api_error.Unauthorized()

    try:
        if redis.get(f"{token_util.user_id}_logout"):
            logger.error(f"[auth-service] user[{token_util.user_id} is logout user")
            raise api_error.Unauthorized()
    except RedisError as err:
        logger.error(f"[auth-service] redis error : {err}")
        raise api_error.ServerError(f"[auth-service] redis error")

    return token
