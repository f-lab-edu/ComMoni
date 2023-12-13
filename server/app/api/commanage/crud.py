from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.commanage.schema import ComManageByUser, ComManageByHost
from app.api.commanage.model import ComManage

from app.common import dictionary_util

from app.api.exception import crud_error

from app.configs.log import logger


class CommanageCRUD:
    """
    Commanage Model에 대한 CURD 구현 클래스
    """

    def __init__(self, session: Session):
        """
        생성자
        :param session: DB Session 객체
        """
        self.session = session

    def create(self, commanage: ComManageByUser) -> ComManage:
        """
        ComManage 객체 생성
        :param commanage: 추가하려는 ComManage 객체
        :return: ComManage
        """
        insert_data = ComManage(**dict(commanage))
        try:
            self.session.add(insert_data)
            self.session.commit()
            self.session.refresh(insert_data)
        except SQLAlchemyError as err:
            logger.error(f"[ComManage]DB Error : {err}")
            self.session.rollback()
            raise crud_error.DatabaseCreateErr()

        return insert_data

    def get(self, commanage: ComManageByHost) -> ComManage:
        """
        ComManage 객체를 가져오기
        :param commanage: get 요청 객체
        :return: ComManage
        """
        try:
            return self.session \
                .query(ComManage) \
                .filter(ComManage.host_id == commanage.host_id) \
                .first()
        except SQLAlchemyError as err:
            logger.error(f"[ComManage]DB Error : {err}")
            raise crud_error.DatabaseGetErr()

    def get_all(self, commanage: ComManageByUser) -> List[ComManage]:
        """
        User ID에 해당하는 모든 ComManage 객체를 가져오기
        :param commanage: get 요청 객체
        :return: List[ComManage]
        """
        try:
            return self.session \
                .query(ComManage) \
                .filter(ComManage.user_id == commanage.user_id) \
                .all()
        except SQLAlchemyError as err:
            logger.error(f"[ComManage]DB Error : {err}")
            raise crud_error.DatabaseGetErr()

    def update(self, update_data: ComManageByHost) -> None:
        """
        ComManage 객체 수정
        :param update_data: 수정하려는 데이터
        :return: None
        """
        # 값이 None인 키 삭제
        filtered_dict = dictionary_util.remove_none(dict(update_data))

        try:
            updated = self.session.query(ComManage) \
                .filter(ComManage.host_id == update_data.host_id) \
                .update(filtered_dict)
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[ComManage]DB Error : {err}")
            self.session.rollback()
            raise crud_error.DatabaseUpdateErr()

        if updated == 0:
            logger.error("[ComManage]Update is none")

    def delete(self, delete_data: ComManageByHost) -> None:
        """
        ComManage 삭제
        :param delete_data: 호스트 아이디가 포함된 삭제 요청 객체
        :return: None
        """
        try:
            deleted = self.session.query(ComManage) \
                .filter(ComManage.host_id == delete_data.host_id) \
                .update({'deleted': True})
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[ComManage]DB Error : {err}")
            self.session.rollback()
            raise crud_error.DatabaseDeleteErr()

        if deleted == 0:
            logger.error("[ComManage]Delete is none")

    def delete_all(self, commanage: ComManageByUser) -> None:
        """
        User ID에 해당하는 모든 ComManage 삭제 처리
        :param commanage: 유저 아이디가 포함된 삭제 요청 객체
        :return: None
        """
        try:
            deleted = self.session.query(ComManage) \
                .filter(ComManage.user_id == commanage.user_id) \
                .update({'deleted': True})
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[ComManage]DB Error : {err}")
            self.session.rollback()
            raise crud_error.DatabaseDeleteErr()

        if deleted == 0:
            logger.error("[ComManage]Delete_all is none")
