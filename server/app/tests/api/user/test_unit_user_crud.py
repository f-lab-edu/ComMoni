import pytest
from unittest import mock

from mock_alchemy.mocking import AlchemyMagicMock, UnifiedAlchemyMagicMock
from sqlalchemy.exc import SQLAlchemyError

from app.api.user.model import User
from app.api.user.schema import UserCreate, UserGet
from app.api.user.crud import UserCRUD

from app.api.exception import crud_error


class TestUserCRUD:
    user_id = "test_user"
    user_pw = "1234567890"
    user_name = "tester"

    def test_create_success(self):
        """데이터 생성 성공"""
        create_user_data = UserCreate(user_id=self.user_id, user_pw=self.user_pw)
        session = AlchemyMagicMock()

        created_user = UserCRUD(session).create(create_user_data)

        assert created_user.user_id == self.user_id
        assert created_user.user_pw == self.user_pw

    def test_create_fail_by_db_error(self):
        """데이터 생성 실패(DB 에러 발생)"""
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        create_user_data = UserCreate(user_id=self.user_id, user_pw=self.user_pw)
        with pytest.raises(crud_error.DatabaseCreateErr):
            UserCRUD(session).create(create_user_data)

    def test_update_success(self):
        """데이터 수정 성공"""
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 1

        update_data = UserGet(user_id=self.user_id)
        UserCRUD(session).update(update_data=update_data)

    def test_update_fail_by_db_error(self):
        """데이터 수정 실패 (DB 에러 발생)"""
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        update_data = UserGet(user_id=self.user_id)

        with pytest.raises(crud_error.DatabaseUpdateErr):
            UserCRUD(session).update(update_data=update_data)

    def test_delete_success(self):
        """데이터 삭제 성공"""
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 1

        delete_data = UserGet(user_id=self.user_id)
        UserCRUD(session).delete(user=delete_data)

    def test_delete_fail_by_db_error(self):
        """데이터 삭제 실패 (DB 에러 발생)"""
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        delete_data = UserGet(user_id=self.user_id)
        with pytest.raises(crud_error.DatabaseDeleteErr):
            UserCRUD(session).delete(user=delete_data)

    def test_get_success(self):
        """데이터 가져오기"""
        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(User),
              mock.call.filter(User.user_id == self.user_id)],
             [User(user_id=self.user_id,
                   user_pw=self.user_pw,
                   user_name=self.user_name,
                   deleted=False)
              ]
             )
        ])

        requset_user_get = UserGet(user_id=self.user_id)
        result = UserCRUD(session).get(requset_user_get)

        assert result.user_id == self.user_id
        assert result.user_pw == self.user_pw
        assert result.user_name == self.user_name
        assert result.deleted is False

    def test_get_fail_with_db_error(self):
        """데이터 가져오기 실패"""
        session = AlchemyMagicMock()
        session.query.side_effect = SQLAlchemyError()

        requset_user_get = UserGet(user_id=self.user_id)

        with pytest.raises(crud_error.DatabaseGetErr):
            UserCRUD(session).get(requset_user_get)
