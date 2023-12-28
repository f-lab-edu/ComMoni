from fastapi import APIRouter, Depends, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from app.api.auth.schema import TokenSet, Token
from app.api.auth.token_util import JwtToken
from app.api.auth.service import get_auth_service, get_jwt_token, AuthService, KEY_USER_ID

from app.api.commanage.schema import ComManageByUser
from app.api.commanage.service import get_commanage_service, CommanageService

API_VERSION = "v1"
API_NAME = "auth"

auth_router = APIRouter(prefix=f"/{API_VERSION}/{API_NAME}")


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenSet)
def login_with_request_form(
        *,
        form_data=Depends(OAuth2PasswordRequestForm),
        temp_login: bool = Form(False),
        auth_service=Depends(get_auth_service)
):
    """
    로그인 및 토큰 생성
    """
    user_id = form_data.username
    user_pw = form_data.password
    auth_service.authenticate(user_id=user_id, user_pw=user_pw)

    return auth_service.create_token_set(user_id=user_id, temp_login=temp_login)


@auth_router.post("/register-commanage", status_code=status.HTTP_200_OK, response_model=Token)
def register_commanage(
        *,
        commanage_data: ComManageByUser,
        token: JwtToken = Depends(get_jwt_token),
        commanage_service: CommanageService = Depends(get_commanage_service),
        auth_service: AuthService = Depends(get_auth_service)
) -> Token:
    commanage_response = commanage_service.create(commanage_data)
    auth_service.verify_access_token(token)
    user_id = token.get_data(KEY_USER_ID)
    host_id = commanage_response.host_id
    return auth_service.create_agent_token(user_id=user_id, host_id=host_id)


@auth_router.get("/refresh-token", status_code=status.HTTP_200_OK, response_model=TokenSet)
def renew_token(
        *,
        token: JwtToken = Depends(get_jwt_token),
        auth_service=Depends(get_auth_service)
) -> TokenSet:
    """
    token 갱신
    """
    auth_service.verify_refresh_token(token)
    return auth_service.renew_token(token)


@auth_router.get("/logout", status_code=status.HTTP_200_OK)
def logout(
        *,
        token: JwtToken = Depends(get_jwt_token),
        auth_service=Depends(get_auth_service)
) -> JSONResponse:
    """
    logout
    """
    auth_service.verify_access_token(token)
    auth_service.remove_token(token)
    return JSONResponse(content={"message": "success"})
