from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.cominfo_schema import ComInfoCreate, ComInfo, ComInfoRTCreate, ComInfoRT
from app.crud.cominfo_crud import CominfoCRUD, CominfoRtCRUD
from app.crud.commanage_crud import CommanageCRUD

router = APIRouter()


@router.post("/", response_model=ComInfo)
def create_cominfo(
        *,
        db: Session = Depends(get_db),
        cominfo: ComInfoCreate
) -> ComInfo:
    """
    ComInfo 객체 추가
    :param db: db Session
    :param cominfo: 추가하려는 ComInfo 객체
    :return: ComInfoCreate 스키마
    """
    if CommanageCRUD(db).get(host_id=cominfo.host_id):
        return CominfoCRUD(db).create(cominfo=cominfo)
    else:
        raise HTTPException(status_code=404, detail=f"host_id[{cominfo.host_id}] is not exist host_id")


@router.get("/", response_model=list[ComInfo])
def get_cominfos(
        *,
        db: Session = Depends(get_db),
        host_id: int,
        skip: int = 0,
        limit: int = 1000,
        start_dt: Optional[datetime] = None,
        end_dt: Optional[datetime] = None
) -> List[ComInfo]:
    """
    ComInfo 값 가져오기
    :param db: db Session
    :param host_id: Host Id 값
    :param skip: 넘기려는 데이터 Row
    :param limit: 가져오려는 Row
    :param start_dt: 시작 날짜/시간
    :param end_dt: 종료 날짜/시간
    :return: List[ComInfoGet] 스키마
    """
    if start_dt or end_dt:
        cominfos = CominfoCRUD(db).get_by_datetime(host_id=host_id, start_dt=start_dt, end_dt=end_dt)
    else:
        cominfos = CominfoCRUD(db).get_multiline(host_id=host_id, skip=skip, limit=limit)

    if cominfos:
        return cominfos
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.put("/realtime", response_model=ComInfoRT)
def put_cominfo_realtime(
        *,
        db: Session = Depends(get_db),
        cominfo: ComInfoRTCreate
) -> ComInfoRT:
    """
    CominfoRT(Real-Time) 값 추가 또는 수정
    :param db: db Session
    :param cominfo: 추가하려는 ComInfo 객체
    :return: ComInfoRT 스키마
    """
    if origin_cominfo := CominfoRtCRUD(db).get(host_id=cominfo.host_id):
        return CominfoRtCRUD(db).update(origin=origin_cominfo, update=cominfo)
    else:
        return CominfoRtCRUD(db).create(cominfo=cominfo)


@router.get("/realtime", response_model=ComInfo)
def get_cominfo_realtime(
        *,
        db: Session = Depends(get_db),
        host_id: int
) -> ComInfoRT:
    """
    CominfoRT(Real-Time) 값 가져오기
    :param db: ㅇb Session
    :param host_id: Host ID 값
    :return: ComInfoRT 스키마
    """
    if cominfo_rt := CominfoRtCRUD(db).get(host_id=host_id):
        return cominfo_rt
    else:
        raise HTTPException(status_code=404, detail=f"host_id[{host_id}] is not exist host_id")
