from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.user.model import User
from app.api.user.schema import UserGet, UserCreate

from app.common import dictionary_util

from app.api.user import exception

from app.configs.log import logger


class UserCRUD:
    """
    User Model에 대한 CURD 구현 클래스
    """

    def __init__(self, session: Session):
        """
        생성자
        :param session: DB Session 객체
        """
        self.session = session

    def create(self, user: UserCreate) -> User:
        """
        User 객체 생성
        :param user: 추가하려는 User 객체
        :return: model.User
        """
        insert_data = User(**dict(user))

        try:
            self.session.add(insert_data)
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[User]DB Err : {err}")
            self.session.rollback()
            raise exception.DatabaseCreateErr()

        return insert_data

    def get(self, user: UserGet) -> User:
        """
        User 객체를 가져오기
        :param user: user 요청 객체
        :return: model.User
        """
        try:
            return self.session \
                .query(User) \
                .filter(User.user_id == user.user_id) \
                .first()
        except SQLAlchemyError as err:
            logger.error(f"[User]DB Err : {err}")
            raise exception.DatabaseGetErr()

    def update(self, update_data: UserGet) -> None:
        """
        User 객체 수정
        :param update_data: 수정하려는 데이터
        :return: None
        """
        # 값이 None인 키 삭제
        filtered_dict = dictionary_util.remove_none(dict(update_data))

        try:
            updated = self.session.query(User) \
                .filter(User.user_id == update_data.user_id) \
                .update(filtered_dict)
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[User]DB Error : {err}")
            self.session.rollback()
            raise exception.DatabaseUpdateErr()

        if updated == 0:
            logger.error(f"[User]Update is None. user_id : {update_data.user_id}")

    def delete(self, user: UserGet) -> None:
        """
        User 삭제
        :param user: 삭제 요청 객체
        :return: None
        """
        try:
            deleted = self.session.query(User) \
                .filter(User.user_id == user.user_id) \
                .update({"deleted": True})
            self.session.commit()
        except SQLAlchemyError as err:
            logger.error(f"[User]DB Err : {err}")
            self.session.rollback()
            raise exception.DatabaseDeleteErr()

        if deleted == 0:
            logger.error(f"[User]Delete is None. user_id : {user.user_id}")
