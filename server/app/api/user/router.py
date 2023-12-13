from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth.service import verify_token
from app.api.user.schema import UserCreate, UserGet, UserResponse, UserStatus
from app.api.user.service import UserService

API_VERSION = "v1"
API_NAME = "user"

user_router = APIRouter(prefix=f"/{API_VERSION}/{API_NAME}")


@user_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
        *,
        db: Session = Depends(get_db),
        user: UserCreate,
        _: str = Depends(verify_token)
) -> UserResponse:
    """
    유저 생성
    :param db: db Session
    :param user: 추가하려는 User 객체
    :return: UserResponse
    """
    return UserService(db=db).create(user)


@user_router.get("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(
        *,
        db: Session = Depends(get_db),
        user_id: str,
        _: str = Depends(verify_token)
) -> UserResponse:
    """
    User ID 값으로 User 값 가져오기
    :param db: db Session
    :param user_id: 찾으려고 하는 유저 객체
    :return: UserResponse
    """
    return UserService(db=db).get(user_id=user_id)


@user_router.get("/{user_id}/status", status_code=status.HTTP_200_OK,
                 response_model=UserStatus)
def get_user_status(
        *,
        db: Session = Depends(get_db),
        user_id: str,
        _: str = Depends(verify_token)
) -> UserStatus:
    """
    User 상태 정보 확인
    :param db: db Session
    :param user_id: 확인 하려는 유저 아이디
    :return: UserStatus
    """
    return UserService(db=db).get_status(user_id=user_id)


@user_router.put("/", status_code=status.HTTP_200_OK)
def update_user(
        *,
        db: Session = Depends(get_db),
        user: UserGet,
        _: str = Depends(verify_token)
):
    """
    User 객체 정보 수정
    :param db: db Session
    :param user: 수정하려는 유저 정보
    :return: JSONResponse
    """
    UserService(db=db).update(user=user)
    return JSONResponse(content={"message": "success"})


@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
        *,
        db: Session = Depends(get_db),
        user_id: str,
        _: str = Depends(verify_token)
):
    """
    User를 삭제
    :param db: db Session
    :param user_id: 삭제하려는 유저 아이디
    :return: JSONResponse
    """
    UserService(db=db).delete(user_id=user_id)
    return JSONResponse(content={"message": "success"})
