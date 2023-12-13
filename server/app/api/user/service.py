from sqlalchemy.orm import Session

from app.api.user.crud import UserCRUD
from app.api.user.schema import UserCreate, UserGet, UserStatus, UserResponse

from app.api import commanage

from app.common.passwd_util import get_password_hash

from app.api.exception import api_error
from app.api.user import exception

from app.configs.log import logger


class UserService:
    """
    User 서비스 로직을 구현한 클래스
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserCreate):
        try:
            result = UserCRUD(self.db).get(user=UserGet(user_id=user.user_id))
        except exception.DatabaseGetErr:
            logger.error(f"[UserService] UserCRUD get error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

        if result:
            logger.error(f"[UserService] user[{user.user_id}] is already existed")
            raise api_error.AlreadyExistedUser(user_id=user.user_id)

        create_data = user
        create_data.user_pw = get_password_hash(password=user.user_pw)

        try:
            created_user = UserCRUD(self.db).create(user=create_data)
        except exception.DatabaseCreateErr:
            logger.error(f"[UserService] UserCRUD create error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

        return UserResponse(user_id=created_user.user_id, user_name=created_user.user_name)

    def get(self, user_id: str):
        """
        User 가져오기
        :param user_id: 사용자 아이디
        :return: User
        """
        try:
            user = UserCRUD(self.db).get(UserGet(user_id=user_id))
        except exception.DatabaseGetErr:
            logger.error(f"[UserService] UserCRUD get error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

        if not user:
            logger.error(f"[UserService] user[{user_id}] is not found")
            raise api_error.UserNotFound(user_id=user_id)

        return UserResponse(user_id=user.user_id, user_name=user.user_name)

    def get_status(self, user_id: str):
        """
        user 상태 정보 가져오기
        :param user_id: 사용자 아이디
        :return: User
        """
        try:
            user = UserCRUD(self.db).get(UserGet(user_id=user_id))
        except exception.DatabaseGetErr:
            logger.error(f"[UserService] UserCRUD get error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

        if not user:
            logger.error(f"[UserService] user[{user_id}] is not found")
            raise api_error.UserNotFound(user_id=user_id)

        return UserStatus(user_id=user.user_id, user_name=user.user_name, deleted=user.deleted)

    def update(self, user: UserGet) -> None:
        """
        User 수정
        :param user: 수정할 사용자 정보
        :return: None
        """
        try:
            result = UserCRUD(self.db).get(user=user)
        except exception.DatabaseGetErr:
            logger.error(f"[UserService] user[{user.user_id}] is already existed")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

        if not result:
            logger.error(f"[UserService] user[{user.user_id}] is not found")
            raise api_error.UserNotFound(user_id=user.user_id)

        try:
            UserCRUD(self.db).update(update_data=user)
        except exception.DatabaseUpdateErr:
            logger.error(f"[UserService] UserCRUD update error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

    def delete(self, user_id: str) -> None:
        """
        User 삭제
        :param user_id: 삭제할 사용자 아이디
        :return: None
        """
        try:
            result = UserCRUD(self.db).get(user=UserGet(user_id=user_id))
        except exception.DatabaseGetErr:
            logger.error(f"[UserService] UserCRUD get error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")

        if not result:
            raise api_error.UserNotFound(user_id=user_id)

        try:
            # User ID 에 해당하는 ComManage 전부 삭제 처리
            commanage.crud.CommanageCRUD(self.db).delete_all(
                commanage=commanage.schema.ComManageByUser(user_id=user_id))
        except commanage.exception.DatabaseDeleteErr:
            logger.error(f"[UserService] CommanageCRUD delete_all error")
            raise api_error.ServerError(f"[UserService] CommanageCRUD error")

        try:
            UserCRUD(self.db).delete(user=UserGet(user_id=user_id))
        except exception.DatabaseDeleteErr:
            logger.error(f"[UserService] UserCRUD delete error")
            raise api_error.ServerError(f"[UserService] UserCRUD error")
