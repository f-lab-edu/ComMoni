from sqlalchemy.orm import Session

from app.api.commanage.schema import ComManageByUser, ComManageByHost, ComManageResponse
from app.api.commanage.crud import CommanageCRUD

from app.api import user

from app.api.exception import api_error
from app.api.commanage import exception

from app.configs.log import logger


class CommanageService:
    """
    Commanage Service 로직 구현 클래스
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, commanage: ComManageByUser):
        """
        commanage 생성
        :param commanage:
        :return:
        """
        try:
            result = user.crud.UserCRUD(self.db).get(
                user.schema.UserGet(user_id=commanage.user_id))
        except user.exception.DatabaseGetErr:
            logger.error(f"[CommanageService] UserCRUD get error")
            raise api_error.ServerError(f"[CommanageService] UserCRUD error")

        if not result:
            logger.error(f"[CommanageService] user[{commanage.user_id}] is not found")
            raise api_error.UserNotFound(user_id=commanage.user_id)

        try:
            created_commanage = CommanageCRUD(self.db).create(commanage=commanage)
        except exception.DatabaseCreateErr:
            logger.error(f"[CommanageService] CommanageCRUD create error")
            raise api_error.ServerError(f"[CommanageService] CommanageCRUD error")

        return ComManageResponse(host_id=created_commanage.host_id)

    def get(self, host_id: int):
        """
        commanage 가져오기
        :param host_id: commanage의 host id
        :return: Commanage
        """
        try:
            result = CommanageCRUD(self.db).get(commanage=ComManageByHost(host_id=host_id))
        except exception.DatabaseGetErr:
            logger.error(f"[CommanageService] CommanageCRUD get error")
            raise api_error.ServerError(f"[CommanageService] CommanageCRUD error")

        if not result:
            logger.error(f"[CommanageService] commanage[hostid={host_id}] is not found")
            raise api_error.CommanageNotFound(host_id=host_id)

        return result

    def get_all(self, user_id: str):
        """
        user_id에 해당하는 모든 commanage 가져오기
        :param user_id: 사용자 아이디
        :return: List[Commanage]
        """
        try:
            commanage = ComManageByUser(user_id=user_id)
            return CommanageCRUD(self.db).get_all(commanage=commanage)
        except exception.DatabaseGetErr:
            logger.error(f"[CommanageService] CommanageCRUD get error")
            raise api_error.ServerError(f"[CommanageService] CommanageCRUD error")

    def update(self, commanage: ComManageByHost) -> None:
        """
        commanage 수정
        :param commanage: 수정할 데이터
        :return: None
        """
        try:
            result = CommanageCRUD(self.db).get(commanage=commanage)
        except exception.DatabaseGetErr:
            logger.error(f"[CommanageService] CommanageCRUD get error")
            raise api_error.ServerError(f"[CommanageService] CommanageCRUD error")

        if not result:
            logger.error(f"[CommanageService] commanage[hostid={commanage.host_id}] is not found")
            raise api_error.CommanageNotFound(host_id=commanage.host_id)

        try:
            CommanageCRUD(self.db).update(update_data=commanage)
        except exception.DatabaseUpdateErr:
            logger.error(f"[CommanageService] CommanageCRUD update error")
            raise api_error.ServerError(f"[CommanageService] CommanageCRUD error")

    def delete(self, host_id: int) -> None:
        """
        commanage 삭제
        :param host_id: 삭제할 commanage의 host id
        :return: None
        """
        try:
            result = CommanageCRUD(self.db).get(commanage=ComManageByHost(host_id=host_id))
        except exception.DatabaseGetErr:
            logger.error(f"[CommanageService] CommanageCRUD get error")
            raise api_error.ServerError(f"[CommanageService] CommanageCRUD error")

        if not result:
            logger.error(f"[CommanageService] commanage[hostid={host_id}] is not found")
            raise api_error.CommanageNotFound(host_id=host_id)

        try:
            CommanageCRUD(self.db).delete(delete_data=ComManageByHost(host_id=host_id))
        except exception.DatabaseDeleteErr:
            logger.error(f"[CommanageService] CommanageCRUD update error")
            raise api_error.ServerError(f"[CommanageService] CommanageCRUD error")
