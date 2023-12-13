from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.api.auth.service import verify_token
from app.api.commanage.schema import ComManage, ComManageByUser, ComManageByHost, ComManageResponse
from app.api.commanage.service import CommanageService

API_VERSION = "v1"
API_NAME = "commanage"

commanage_router = APIRouter(prefix=f"/{API_VERSION}/{API_NAME}")


@commanage_router.post("/", status_code=status.HTTP_201_CREATED)
def create_commanage(
        *,
        db: Session = Depends(get_db),
        commanage: ComManageByUser,
        _: str = Depends(verify_token)
) -> ComManageResponse:
    """
    ComManage 생성
    :param db: db Session
    :param commanage: 추가하려는 ComManage 객체
    :return: ComManageResponse
    """
    return CommanageService(db=db).create(commanage=commanage)


@commanage_router.get("/{host_id}", status_code=status.HTTP_200_OK, response_model=ComManage)
def get_commanage(
        *,
        db: Session = Depends(get_db),
        host_id: int,
        _: str = Depends(verify_token)
) -> ComManage:
    """
    Host ID로 ComManage 가져오기
    :param db: db Session
    :param host_id: Host ID 값
    :return: ComManage 스키마
    """
    return CommanageService(db=db).get(host_id=host_id)


@commanage_router.get("/all/{user_id}", status_code=status.HTTP_200_OK, response_model=list[ComManage])
def get_all_commanage(
        *,
        db: Session = Depends(get_db),
        user_id: str,
        _: str = Depends(verify_token)
) -> List[ComManage]:
    """
    User ID로 ComManage 가져오기
    :param db: db Session
    :param user_id: User ID 값
    :return: List[ComManage] 스키마
    """
    return CommanageService(db=db).get_all(user_id=user_id)


@commanage_router.put("/", status_code=status.HTTP_200_OK)
def update_commanage(
        *,
        db: Session = Depends(get_db),
        commanage: ComManageByHost,
        _: str = Depends(verify_token)
) -> JSONResponse:
    """
    ComManage 객체 수정
    :param db: db Session
    :param commanage: 수정하려는 ComManage 객체
    :return: JSONResponse
    """
    CommanageService(db=db).update(commanage=commanage)
    return JSONResponse(content={"message": "success"})


@commanage_router.delete("/{host_id}", status_code=status.HTTP_200_OK)
def delete_commanage(
        *,
        db: Session = Depends(get_db),
        host_id: int,
        _: str = Depends(verify_token)
) -> JSONResponse:
    """
    ComManage 삭제xs
    :param db: db Session
    :param commanage: 삭제하려는 ComManage 객체
    :return: JSONResponse
    """
    CommanageService(db=db).delete(host_id=host_id)
    return JSONResponse(content={"message": "success"})
