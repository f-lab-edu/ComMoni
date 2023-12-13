import pytest
from fastapi import status
from datetime import datetime

from app.api import commanage
from app.api.cominfo.service import CominfoService, CominfoRTService
from app.api.cominfo.model import ComInfo, ComInfoRT
from app.api.cominfo.schema import ComInfoGet, ComInfoCreate, ComInfoRTUpdate, ComInfoRTGet

from app.api.exception import crud_error, api_error


class TestCominfoAPI:
    host_id = 1
    cpu_utilization = 10.1
    memory_utilization = 20.2
    disk_utilization = 30.3
    make_datetime = datetime.now()

    start_dt = make_datetime
    end_et = make_datetime
    skip = 5
    limit = 100

    create_data = {
        "host_id": host_id,
        "cpu_utilization": cpu_utilization,
        "memory_utilization": memory_utilization,
        "disk_utilization": disk_utilization,
        "make_datetime": make_datetime
    }

    commanage_model = commanage.model.ComManage(host_id=host_id)
    cominfo_get_schema = ComInfoGet(host_id=host_id)
    cominfo_create_schema = ComInfoCreate(
        host_id=host_id,
        cpu_utilization=cpu_utilization,
        memory_utilization=memory_utilization,
        disk_utilization=disk_utilization,
        make_datetime=make_datetime
    )
    cominfo_schema = [ComInfo(
        host_id=host_id,
        cpu_utilization=cpu_utilization,
        memory_utilization=memory_utilization,
        disk_utilization=disk_utilization,
        make_datetime=make_datetime
    )]

    def test_create_success(self, mocker):
        """
        Cominfo 생성 테스트 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=self.commanage_model)
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.create', return_value=self.cominfo_get_schema)

        result = CominfoService(db).create(cominfo=self.cominfo_create_schema)
        assert result == self.cominfo_get_schema

    def test_create_fail_1(self, mocker):
        """
        Cominfo 생성 테스트 실패, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CominfoService(db).create(cominfo=self.cominfo_create_schema)

    def test_create_fail_2(self, mocker):
        """
        Cominfo 생성 테스트 실패, Commanage 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=None)

        with pytest.raises(api_error.CommanageNotFound):
            CominfoService(db).create(cominfo=self.cominfo_create_schema)

    def test_create_fail_3(self, mocker):
        """
        Cominfo 생성 테스트 실패, DB create error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.commanage.crud.CommanageCRUD.get', return_value=self.commanage_model)
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.create', return_value=None) \
            .side_effect = crud_error.DatabaseCreateErr

        with pytest.raises(api_error.ServerError):
            CominfoService(db).create(cominfo=self.cominfo_create_schema)

    def test_get_success_1(self, mocker):
        """
        Cominfo 가져오기 성공, 시작 날짜만 있는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_by_datetime', return_value=self.cominfo_schema)

        result = CominfoService(db).get(host_id=self.host_id, start_dt=self.start_dt)
        assert result == self.cominfo_schema

    def test_get_success_2(self, mocker):
        """
        Cominfo 가져오기 성공, 종료 날짜만 있는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_by_datetime', return_value=self.cominfo_schema)

        result = CominfoService(db).get(host_id=self.host_id, end_dt=self.end_et)
        assert result == self.cominfo_schema

    def test_get_success_3(self, mocker):
        """
        Cominfo 가져오기 성공, 시작, 종료 날짜 있는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_by_datetime', return_value=self.cominfo_schema)

        result = CominfoService(db).get(host_id=self.host_id, start_dt=self.start_dt, end_dt=self.end_et)
        assert result == self.cominfo_schema

    def test_get_success_4(self, mocker):
        """
        Cominfo 가져오기 skip 있는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_multiline', return_value=self.cominfo_schema)

        result = CominfoService(db).get(host_id=self.host_id, skip=self.skip)
        assert result == self.cominfo_schema

    def test_get_success_5(self, mocker):
        """
        Cominfo 가져오기 limit 있는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_multiline', return_value=self.cominfo_schema)

        result = CominfoService(db).get(host_id=self.host_id, limit=self.limit)
        assert result == self.cominfo_schema

    def test_get_success_6(self, mocker):
        """
        Cominfo 가져오기 성공, skip, limit 있는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_multiline', return_value=self.cominfo_schema)

        result = CominfoService(db).get(host_id=self.host_id, skip=self.skip, limit=self.limit)
        assert result == self.cominfo_schema

    def test_get_fail_1(self, mocker):
        """
        Cominfo 가져오기 실패, 시작 날짜만 있는 경우, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_by_datetime', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CominfoService(db).get(host_id=self.host_id, start_dt=self.start_dt)

    def test_get_fail_2(self, mocker):
        """
        Cominfo 가져오기 실패, 종료 날짜만 있는 경우, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_by_datetime', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CominfoService(db).get(host_id=self.host_id, end_dt=self.end_et)

    def test_get_fail_3(self, mocker):
        """
        Cominfo 가져오기 실패, 시작, 종료 날짜 있는 경우, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_by_datetime', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CominfoService(db).get(host_id=self.host_id, start_dt=self.start_dt, end_dt=self.end_et)

    def test_get_fail_4(self, mocker):
        """
        Cominfo 가져오기 실패, 시작 날짜만 있는 경우, 데이터가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_by_datetime', return_value=None)

        with pytest.raises(api_error.ItemNotFound):
            CominfoService(db).get(host_id=self.host_id, start_dt=self.start_dt)

    def test_get_fail_5(self, mocker):
        """
        Cominfo 가져오기 실패, 종료 날짜만 있는 경우, 데이터가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_by_datetime', return_value=None)

        with pytest.raises(api_error.ItemNotFound):
            CominfoService(db).get(host_id=self.host_id, end_dt=self.end_et)

    def test_get_fail_6(self, mocker):
        """
        Cominfo 가져오기 실패, 시작, 종료 날짜 있는 경우, 데이터가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_by_datetime', return_value=None)

        with pytest.raises(api_error.ItemNotFound):
            CominfoService(db).get(host_id=self.host_id, start_dt=self.start_dt, end_dt=self.end_et)

    def test_get_fail_7(self, mocker):
        """
        Cominfo 가져오기 실패, skip 있는 경우, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_multiline', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CominfoService(db).get(host_id=self.host_id, skip=self.skip)

    def test_get_fail_8(self, mocker):
        """
        Cominfo 가져오기 실패, limit 있는 경우, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_multiline', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CominfoService(db).get(host_id=self.host_id, limit=self.limit)

    def test_get_fail_9(self, mocker):
        """
        Cominfo 가져오기 실패, skip, limit 있는 경우, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_multiline', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CominfoService(db).get(host_id=self.host_id, skip=self.skip, limit=self.limit)

    def test_get_fail_10(self, mocker):
        """
        Cominfo 가져오기 실패, skip 있는 경우, 데이터가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_multiline', return_value=None)

        with pytest.raises(api_error.ItemNotFound):
            CominfoService(db).get(host_id=self.host_id, skip=self.skip)

    def test_get_fail_11(self, mocker):
        """
        Cominfo 가져오기 실패, limit 있는 경우, 데이터가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_multiline', return_value=None)

        with pytest.raises(api_error.ItemNotFound):
            CominfoService(db).get(host_id=self.host_id, limit=self.limit)

    def test_get_fail_12(self, mocker):
        """
        Cominfo 가져오기 실패, skip, limit 있는 경우, 데이터가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoCRUD.get_multiline', return_value=None)

        with pytest.raises(api_error.ItemNotFound):
            CominfoService(db).get(host_id=self.host_id, skip=self.skip, limit=self.limit)


class TestCominfoRtAPI:
    host_id = 1
    cpu_utilization = 10.1
    memory_utilization = 20.2
    disk_utilization = 30.3
    make_datetime = datetime.now()
    update_datetime = datetime.now()

    cominfort_model = ComInfoRT(
        host_id=host_id,
        cpu_utilization=cpu_utilization,
        memory_utilization=memory_utilization,
        disk_utilization=disk_utilization,
    )

    create_data = {
        "host_id": host_id,
        "cpu_utilization": cpu_utilization,
        "memory_utilization": memory_utilization,
        "disk_utilization": disk_utilization,
    }
    cominfort_get_schema = ComInfoRTGet(host_id=host_id)
    cominfort_update_schema = ComInfoRTUpdate(
        host_id=host_id,
        cpu_utilization=cpu_utilization,
        memory_utilization=memory_utilization,
        disk_utilization=disk_utilization,
        make_datetime=make_datetime,
        update_datetime=update_datetime,
    )

    def test_put_succces_1(self, mocker):
        """
        comfinort put 테스트 성공 (생성)
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.get', return_value=None)
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.create', return_value=self.cominfort_model)

        CominfoRTService(db).put(cominfo_rt=self.cominfort_get_schema)

    def test_put_succces_2(self, mocker):
        """
        comfinort put 테스트 성공 (업데이트)
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.get', return_value=self.cominfort_model)
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.update', return_value=self.cominfort_model)

        CominfoRTService(db).put(cominfo_rt=self.cominfort_get_schema)

    def test_put_fail_1(self, mocker):
        """
        comfinort put 테스트 실패 (생성), DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.get', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CominfoRTService(db).put(cominfo_rt=self.cominfort_get_schema)

    def test_put_fail_2(self, mocker):
        """
        comfinort put 테스트 실패 (수정), DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.get', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CominfoRTService(db).put(cominfo_rt=self.cominfort_update_schema)

    def test_put_fail_3(self, mocker):
        """
        comfinort put 테스트 실패 (생성), DB create error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.get', return_value=None)
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.create', return_value=None) \
            .side_effect = crud_error.DatabaseCreateErr

        with pytest.raises(api_error.ServerError):
            CominfoRTService(db).put(cominfo_rt=self.cominfort_get_schema)

    def test_put_fail_4(self, mocker):
        """
        comfinort put 테스트 실패 (수정), DB update error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.get', return_value=self.cominfort_model)
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.update', return_value=None) \
            .side_effect = crud_error.DatabaseUpdateErr

        with pytest.raises(api_error.ServerError):
            CominfoRTService(db).put(cominfo_rt=self.cominfort_update_schema)

    def test_get_success(self, mocker):
        """
        cominfort 가져오기 성공
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.get', return_value=self.cominfort_get_schema)

        result = CominfoRTService(db).get(host_id=self.host_id)
        assert result == self.cominfort_get_schema

    def test_get_fail_1(self, mocker):
        """
        cominfort 가져오기 실패, DB get error 발생
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.get', return_value=None) \
            .side_effect = crud_error.DatabaseGetErr

        with pytest.raises(api_error.ServerError):
            CominfoRTService(db).get(host_id=self.host_id)

    def test_get_fail_2(self, mocker):
        """
        cominfort 가져오기 실패, 데이터가 없는 경우
        """
        db = mocker.MagicMock()
        mocker.patch('app.api.cominfo.crud.CominfoRtCRUD.get', return_value=None)

        with pytest.raises(api_error.ItemNotFound):
            CominfoRTService(db).get(host_id=self.host_id)
