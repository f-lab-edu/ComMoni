from typing import Optional, Union
from datetime import datetime

from sqlalchemy.orm import Session

from app.api.cominfo.schema import ComInfoCreate, ComInfoGet
from app.api.cominfo.schema import ComInfoRTGet, ComInfoRTUpdate
from app.api.cominfo.crud import CominfoCRUD
from app.api.cominfo.crud import CominfoRtCRUD

from app.api import commanage

from app.api.exception import api_error
from app.api.cominfo import exception

from app.configs.log import logger


class CominfoService:
    """
    Cominfo 서비스 로직 구현 클래스
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, cominfo: ComInfoCreate) -> ComInfoGet:
        """
        cominfo 생성
        :param cominfo: 생성할 cominfo
        :return: ComInfoGet
        """
        try:
            result = commanage.crud.CommanageCRUD(self.db).get(
                commanage=commanage.schema.ComManageByHost(host_id=cominfo.host_id))
        except commanage.exception.DatabaseGetErr:
            logger.error(f"[CominfoService] CommanageCRUD get error")
            raise api_error.ServerError(f"[CominfoService] CommanageCRUD error")

        if not result:
            logger.error(f"[CominfoService] commanage[hostid = {cominfo.host_id}] is not found")
            raise api_error.CommanageNotFound(host_id=cominfo.host_id)

        try:
            created_cominfo = CominfoCRUD(self.db).create(cominfo=cominfo)
        except exception.DatabaseCreateErr:
            logger.error(f"[CominfoService] CominfoCRUD create error")
            raise api_error.ServerError(f"[CominfoService] CommanageCRUD error")

        return ComInfoGet(host_id=created_cominfo.host_id)

    def get(self,
            host_id: int,
            skip: int = 0,
            limit: int = 50,
            start_dt: Optional[datetime] = None,
            end_dt: Optional[datetime] = None):
        """
        cominfo 가져오기
        :param host_id: commanage의 host id
        :param skip: 건너뛸 index 값
        :param limit: 가져올 라인 수
        :param start_dt: 생성일(범위 시작)
        :param end_dt: 생성일(범위 끝)
        :return: List[Cominfo]
        """
        try:
            if start_dt or end_dt:
                cominfos = CominfoCRUD(self.db).get_by_datetime(
                    cominfo=ComInfoGet(host_id=host_id), start_dt=start_dt, end_dt=end_dt)
            else:
                cominfos = CominfoCRUD(self.db).get_multiline(
                    cominfo=ComInfoGet(host_id=host_id), skip=skip, limit=limit)
        except exception.DatabaseGetErr:
            logger.error(f"[CominfoService] CominfoCRUD get error")
            raise api_error.ServerError(f"[CominfoService] CominfoCRUD error")

        if not cominfos:
            logger.error(f"[CominfoService] cominfo is not found")
            raise api_error.ItemNotFound()

        return cominfos


class CominfoRTService:
    """
    CominfoRT 서비스 로직 구현 클래스
    """

    def __init__(self, db):
        self.db = db

    def put(self, cominfo_rt: Union[ComInfoRTUpdate, ComInfoRTGet]) -> None:
        """
        ComInfoRT
        :param cominfo_rt: 생성/수정 할 cominfo 데이터
        :return: None
        """
        try:
            result = CominfoRtCRUD(self.db).get(
                cominfo=ComInfoRTGet(host_id=cominfo_rt.host_id))
        except exception.DatabaseGetErr:
            logger.error(f"[CominfoRTService] CominfoRtCRUD get error")
            raise api_error.ServerError(f"[CominfoRTService] CominfoRtCRUD error")

        if not result:
            try:
                CominfoRtCRUD(self.db).create(cominfo=cominfo_rt)
            except exception.DatabaseCreateErr:
                logger.error(f"[CominfoRTService] CominfoRtCRUD create error")
                raise api_error.ServerError(f"[CominfoRTService] CominfoRtCRUD error")
        else:
            try:
                CominfoRtCRUD(self.db).update(update_data=cominfo_rt)
            except exception.DatabaseUpdateErr:
                logger.error(f"[CominfoRTService] CominfoRtCRUD update error")
                raise api_error.ServerError(f"[CominfoRTService] CominfoRtCRUD error")

    def get(self, host_id: int) -> ComInfoRTGet:
        """
        cominfort 가져오기
        :param host_id: commanage의 host_id
        :return: ComInfoRTGet 스키마
        """
        try:
            result = CominfoRtCRUD(self.db).get(
                cominfo=ComInfoRTGet(host_id=host_id))
        except exception.DatabaseGetErr:
            logger.error(f"[CominfoRTService] CominfoRtCRUD get error")
            raise api_error.ServerError(f"[CominfoRTService] CominfoRtCRUD error")

        if not result:
            logger.error(f"[CominfoRTService] commanage[hostid = {host_id}] is not found")
            raise api_error.ItemNotFound()

        return result
