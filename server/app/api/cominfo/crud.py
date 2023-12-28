from typing import List
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.cominfo.schema import ComInfoCreate, ComInfoGet, ComInfoRTGet, ComInfoRTUpdate
from app.api.cominfo.model import ComInfo, ComInfoRT

from app.api.exception import crud_error

from app.configs.log import logger


class CominfoCRUD:
    """
    Cominfo Model에 대한 CURD 구현 클래스
    """

    def __init__(self, session: Session):
        """
        생성자
        :param session: DB Session 객체
        """
        self.session = session

    def create(self, cominfo: ComInfoCreate) -> ComInfo:
        """
        ComInfo 객체 생성
        :param cominfo: 추가하려는 ComInfo 객체
        :return: ComInfo
        """
        insert_data = ComInfo(**dict(cominfo))
        try:
            self.session.add(insert_data)
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[ComInfo]DB Error : {err}")
            self.session.rollback()
            raise crud_error.DatabaseCreateErr()

        return insert_data

    def get_by_datetime(self, cominfo: ComInfoGet, start_dt: datetime = None, end_dt: datetime = None) \
            -> List[ComInfo]:
        """
        시작 날짜 ~ 종료 날짜 사이의 ComInfo 객체를 가져오기
        :param cominfo: Host ID 값이 포함된 객체
        :param start_dt: 시작 날짜/시간
        :param end_dt: 종료 날짜/시간
        :return: List[ComInfo]
        """
        try:
            query = self.session.query(ComInfo) \
                .filter(ComInfo.host_id == cominfo.host_id)

            if start_dt:
                query = query.filter(ComInfo.make_datetime >= start_dt)

            if end_dt:
                query = query.filter(ComInfo.make_datetime <= end_dt)

            return query.all()
        except SQLAlchemyError as err:
            logger.error(f"[ComInfo]DB Error : {err}")
            raise crud_error.DatabaseGetErr()

    def get_multiline(self, cominfo: ComInfoGet, skip: int = 0, limit: int = 1000) -> List[ComInfo]:
        """
        ComInfo 객체를 가져오기
        :param cominfo: Host ID 값이 포함된 객체
        :param skip: 넘기려는 데이터 Row
        :param limit: 가져오려는 Row
        :return: List[ComInfo]
        """
        try:
            return self.session \
                .query(ComInfo) \
                .filter(ComInfo.host_id == cominfo.host_id) \
                .offset(skip) \
                .limit(limit) \
                .all()
        except SQLAlchemyError as err:
            logger.error(f"[ComInfo]DB Error : {err}")
            raise crud_error.DatabaseGetErr()


class CominfoRtCRUD:
    """
    CominfoRT(Real-Time) Model에 대한 CURD 구현 클래스
    """

    def __init__(self, session: Session):
        self.session = session

    def create(self, cominfo: ComInfoRTGet) -> ComInfoRTGet:
        """
        ComInfoRT 객체를 생성
        :param cominfo: 생성하려는 ComInfoRT 객체
        :return: ComInfoRT
        """
        insert_data = ComInfoRT(**dict(cominfo))
        try:
            self.session.add(insert_data)
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[ComInfoRT]DB Error : {err}")
            self.session.rollback()
            raise crud_error.DatabaseCreateErr()

        return insert_data

    def get(self, cominfo: ComInfoRTGet) -> ComInfoRTGet:
        """
        Host ID에 해당하는 ComInfoRT 데이터 읽기
        :param cominfo: Host ID 값이 포함된 객체
        :return: ComInfoRT
        """
        try:
            return self.session \
                .query(ComInfoRT) \
                .filter(ComInfoRT.host_id == cominfo.host_id) \
                .first()
        except SQLAlchemyError as err:
            logger.error(f"[ComInfoRT]DB Error : {err}")
            raise crud_error.DatabaseGetErr()

    def update(self, update_data: ComInfoRTUpdate) -> None:
        """
        ComInfoRt 객체 수정
        :param update_data: 수정하려는 데이터
        :return: None
        """

        try:
            updated = self.session.query(ComInfoRT) \
                .filter(ComInfoRT.host_id == update_data.host_id) \
                .update(dict(update_data))
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[ComInfoRT]DB Error : {err}")
            self.session.rollback()
            raise crud_error.DatabaseUpdateErr()

        if updated == 0:
            logger.error("[ComInfoRT]Delete is none")
