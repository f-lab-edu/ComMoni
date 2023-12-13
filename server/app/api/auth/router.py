from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from redis import Redis

from app.database import get_db
from app.common.redis_util import get_redis
from app.api.auth.service import verify_token

from app.api.auth.schema import Token
from app.api.auth import service

API_VERSION = "v1"
API_NAME = "auth"

auth_router = APIRouter(prefix=f"/{API_VERSION}/{API_NAME}")


@auth_router.post("/login", response_model=Token)
def login_for_token(
        *,
        form_data=Depends(OAuth2PasswordRequestForm),
        host_id: int = Form(),
        db: Session = Depends(get_db),
        redis: Redis = Depends(get_redis)
):
    """
    로그인 및 토큰 생성
    :param form_data: OAuth2 요청 form
    :param host_id: host id 값
    :param db: db session
    :param redis: redis session
    :return: Token 스키마
    """
    user_id = form_data.username
    user_pw = form_data.password
    service.authenticate(user_id=user_id, user_pw=user_pw, db=db)
    return service.create_token(user_id=user_id, host_id=host_id,
                                db=db, redis=redis)


@auth_router.get("/refresh-token", response_model=Token)
def renew_token(
        *,
        token: str = Depends(verify_token),
        redis: Redis = Depends(get_redis)
) -> Token:
    """
    token 갱신
    :param token: 토큰
    :param redis: redis session
    :return: Token
    """
    return service.renew_token(token=token, redis=redis)


@auth_router.get("/logout")
def logout(
        *,
        token: str = Depends(verify_token),
        redis: Redis = Depends(get_redis)
) -> JSONResponse:
    """
    logout
    :param token: 토큰
    :param redis: redis session
    :return: JSONResponse
    """
    service.remove_token(token=token, redis=redis)
    return JSONResponse(content={"message": "success"})
