import pytest

from app.api import user
from app.api.commanage.service import CommanageService
from app.api.commanage.model import ComManage
from app.api.commanage.schema import ComManageResponse, ComManageByHost, ComManageByUser

from app.api.commanage import exception
from app.api.exception import api_error


class TestCommanageAPI:
    user_id = "test_user"
    host_id = 1
    host_name = "tester"
    host_ip = "127.0.0.1"
    memory = "32G"
    disk = "512G"
    deleted = False
    user_name = "tester"

    create_data = {
        "user_id": user_id,
        "host_id": host_id,
        "host_name": host_name,
        "host_ip": host_ip,
        "memory": memory,
        "disk": disk,
        "deleted": deleted
    }

    update_data = {
        "user_id": user_id,
        "host_id": host_id,
        "host_name": host_name,
        "host_ip": host_ip,
        "memory": memory,
        "disk": disk,
        "deleted": deleted
    }

    user_model = user.model.User(user_id=user_id, user_name=user_name)
    commanage_model = ComManage(
        user_id=user_id,
        host_id=host_id,
        host_name=host_name,
        host_ip=host_ip,
        memory=memory,
        disk=disk,
        deleted=deleted
    )
    commanage_by_user_schema = ComManageByUser(user_id=user_id)
    commanage_by_host_schema = ComManageByHost(host_id=host_id)
    commanage_response_schema = ComManageResponse(host_id=host_id)

    def test_create_success(self, mocker):
        """
        Commaange 생성 테스트 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_model)
        mocker.patch('app.api.commanage.crud.CommanageCRUD.create', return_value=self.commanage_model)

        result = CommanageService(db).create(commanage=self.commanage_by_user_schema)

        assert result == self.commanage_response_schema

    def test_create_fail_1(self, mocker):
        """
        Commanage 생성 테스트 실패. User DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None) \
            .side_effect = user.exception.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CommanageService(db).create(commanage=self.commanage_by_user_schema)

    def test_create_fail_2(self, mocker):
        """
        Commanage 생성 테스트 실패. User 가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=None)

        with pytest.raises(api_error.UserNotFound):
            CommanageService(db).create(commanage=self.commanage_by_user_schema)

    def test_create_fail_3(self, mocker):
        """
        Commaange 생성 실패, DB create error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.user.crud.UserCRUD.get', return_value=self.user_model)
        mocker.patch('app.api.commanage.crud.CommanageCRUD.create', return_value=None) \
            .side_effect = exception.DatabaseCreateErr

        with pytest.raises(api_error.ServerError):
            CommanageService(db).create(commanage=self.commanage_by_user_schema)

    def test_get_success(self, mocker):
        """
        host_id로 Commaange 가져오기 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=self.commanage_model)

        result = CommanageService(db).get(host_id=self.host_id)
        assert result == self.commanage_model

    def test_get_fail(self, mocker):
        """
          host_id로 Commaange 가져오기 실패
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=None) \
            .side_effect = exception.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CommanageService(db).get(host_id=self.host_id)

    def test_get_all_success(self, mocker):
        """
        user_id로 Commaange 가져오기 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get_all', return_value=[self.commanage_model])

        result = CommanageService(db).get_all(user_id=self.user_id)
        assert result == [self.commanage_model]

    def test_get_all_fail(self, mocker):
        """
        user_id로 Commaange 가져오기 실패
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get_all', return_value=None) \
            .side_effect = exception.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CommanageService(db).get_all(user_id=self.user_id)

    def test_update_success(self, mocker):
        """
        Commanage 정보 업데이트 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=self.commanage_model)
        mocker.patch('app.api.commanage.crud.CommanageCRUD.update')

        CommanageService(db).update(commanage=self.commanage_by_host_schema)

    def test_update_fail_1(self, mocker):
        """
        Commanage 정보 업데이트 실패, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=None) \
            .side_effect = exception.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CommanageService(db).update(commanage=self.commanage_by_host_schema)

    def test_update_fail_2(self, mocker):
        """
        Commanage 정보 업데이트 실패, Commanage가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=None)

        with pytest.raises(api_error.CommanageNotFound):
            CommanageService(db).update(commanage=self.commanage_by_host_schema)

    def test_update_fail_3(self, mocker):
        """
        Commanage 정보 업데이트 실패, DB update error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=self.commanage_model)
        mocker.patch('app.api.commanage.crud.CommanageCRUD.update') \
            .side_effect = exception.DatabaseUpdateErr

        with pytest.raises(api_error.ServerError):
            CommanageService(db).update(commanage=self.commanage_by_host_schema)

    def test_delete_success(self, mocker):
        """
        Commanage 정보 삭제 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=self.host_id)
        mocker.patch('app.api.commanage.crud.CommanageCRUD.delete')

        CommanageService(db).delete(host_id=self.host_id)

    def test_delete_fail_1(self, mocker):
        """
        Commanage 정보 삭제 실패, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=None) \
            .side_effect = exception.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CommanageService(db).delete(host_id=self.host_id)

    def test_delete_fail_2(self, mocker):
        """
        Commanage 정보 삭제 실패, Commanage가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=None)

        with pytest.raises(api_error.CommanageNotFound):
            CommanageService(db).delete(host_id=self.host_id)

    def test_delete_fail_3(self, mocker):
        """
        Commanage 정보 삭제 실패, DB delete error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=self.commanage_model)
        mocker.patch('app.api.commanage.crud.CommanageCRUD.delete') \
            .side_effect = exception.DatabaseDeleteErr

        with pytest.raises(api_error.ServerError):
            CommanageService(db).delete(host_id=self.host_id)
