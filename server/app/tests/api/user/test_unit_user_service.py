import pytest

from app.api import commanage
from app.api.user.service import UserService
from app.api.user.model import User
from app.api.user.schema import UserResponse, UserStatus, UserGet, UserCreate

from app.api.exception import api_error, crud_error


class TestUserService:
    user_id = "test_user"
    user_pw = "1234567890"
    user_name = "tester"

    create_data = {
        "user_id": user_id,
        "user_pw": user_pw,
        "user_name": user_name
    }

    update_data = {
        "user_id": user_id,
        "user_pw": user_pw,
        "user_name": user_name
    }

    user_model = User(user_id=user_id, user_name=user_name)
    user_get_schema = UserGet(user_id=user_id)
    user_create_schema = UserCreate(user_id=user_id, user_pw=user_pw)
    user_response_schema = UserResponse(user_id=user_id, user_name=user_name)
    user_status_schema = UserStatus(user_id=user_id, user_name=user_name, deleted=False)

    def test_create_success(self, mocker):
        """
        유저 생성 테스트
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)
        mocker.patch('app.api.user.crud.UserCRUD.create', return_value=self.user_model)

        result = UserService(db).create(user=self.user_create_schema)

        assert result == self.user_response_schema

    def test_create_fail_1(self, mocker):
        """
        유저 생성 테스트 실패. DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr()

        with pytest.raises(api_error.ServerError):
            UserService(db).create(user=self.user_create_schema)

    def test_create_fail_2(self, mocker):
        """
        유저 생성 테스트 실패. 이미 유저가 있는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_model)

        with pytest.raises(api_error.AlreadyExistedUser):
            UserService(db).create(user=self.user_create_schema)

    def test_create_fail_3(self, mocker):
        """
        유저 생성 테스트 실패. DB create error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)
        mocker.patch('app.api.user.crud.UserCRUD.create', return_value=self.user_model) \
            .side_effect = crud_error.DatabaseCreateErr

        with pytest.raises(api_error.ServerError):
            UserService(db).create(user=self.user_create_schema)

    def test_get_success(self, mocker):
        """
        유저 정보 가져오기 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_response_schema)

        result = UserService(db).get(user_id=self.user_id)

        assert result == self.user_response_schema

    def test_get_fail_1(self, mocker):
        """
        유저 정보 가져오기 실패, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            UserService(db).get(user_id=self.user_id)

    def test_get_fail_2(self, mocker):
        """
        유저 정보 가져오기 실패, 유저가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)

        with pytest.raises(api_error.UserNotFound):
            UserService(db).get(user_id=self.user_id)

    def test_get_status_success(self, mocker):
        """
        유저 상태 정보 가져오기 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_status_schema)

        result = UserService(db).get_status(user_id=self.user_id)

        assert result == self.user_status_schema

    def test_get_status_fail_1(self, mocker):
        """
        유저 상태 정보 가져오기 실패, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            UserService(db).get_status(user_id=self.user_id)

    def test_get_status_fail_2(self, mocker):
        """
        유저 상태 정보 가져오기 실패, 유저가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)

        with pytest.raises(api_error.UserNotFound):
            UserService(db).get_status(user_id=self.user_id)

    def test_update_success(self, mocker):
        """
        유저 정보 업데이트 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_response_schema)

        UserService(db).update(user=self.user_get_schema)

    def test_update_fail_1(self, mocker):
        """
        유저 정보 업데이트 실패, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            UserService(db).update(user=self.user_get_schema)

    def test_update_fail_2(self, mocker):
        """
        유저 정보 업데이트 실패, 유저가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)

        with pytest.raises(api_error.UserNotFound):
            UserService(db).update(user=self.user_get_schema)

    def test_update_fail_3(self, mocker):
        """
        유저 정보 업데이트 실패, DB update error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_response_schema)
        mocker.patch('app.api.user.crud.UserCRUD.update', return_value=None) \
            .side_effect = crud_error.DatabaseUpdateErr

        with pytest.raises(api_error.ServerError):
            UserService(db).update(user=self.user_get_schema)

    def test_delete_success(self, mocker):
        """
        유저 삭제 성공, 유저에 연관된 commanage 데이터 전부 삭제 처리
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_response_schema)
        mocker.patch('app.api.commanage.crud.CommanageCRUD.delete_all')

        UserService(db).delete(user_id=self.user_id)

    def test_delete_fail_1(self, mocker):
        """
        유저 삭제 실패, 유저 get DB error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            UserService(db).delete(user_id=self.user_id)

    def test_delete_fail_2(self, mocker):
        """
        유저 삭제 실패, 유저가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)

        with pytest.raises(api_error.UserNotFound):
            UserService(db).delete(user_id=self.user_id)

    def test_delete_fail_3(self, mocker):
        """
        유저 삭제 실패, 유저에 연관된 commanage 삭제 실패
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_response_schema)
        mocker.patch('app.api.commanage.crud.CommanageCRUD.delete_all') \
            .side_effect = crud_error.DatabaseDeleteErr

        with pytest.raises(api_error.ServerError):
            UserService(db).delete(user_id=self.user_id)

    def test_delete_fail_4(self, mocker):
        """
        유저 삭제 실패, 유저 DB delete error
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_response_schema)
        mocker.patch('app.api.commanage.crud.CommanageCRUD.delete_all')
        mocker.patch('app.api.user.crud.UserCRUD.delete') \
            .side_effect = crud_error.DatabaseDeleteErr

        with pytest.raises(api_error.ServerError):
            UserService(db).delete(user_id=self.user_id)
