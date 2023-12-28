from unittest import mock
from datetime import datetime

import pytest
from mock_alchemy.mocking import AlchemyMagicMock, UnifiedAlchemyMagicMock
from sqlalchemy.exc import SQLAlchemyError

from app.api.cominfo.model import ComInfo, ComInfoRT
from app.api.cominfo.schema import ComInfoGet, ComInfoCreate, ComInfoRTGet, ComInfoRTUpdate
from app.api.cominfo.crud import CominfoCRUD, CominfoRtCRUD

from app.api.exception import crud_error


class TestCominfoCRUD:
    host_id = 1
    cpu_utilization = 20.5
    memory_utilization = 30.0
    disk_utilization = 40.3
    make_datetime = datetime.now()

    def test_create_success(self):
        """데이터 생성 성공"""
        session = AlchemyMagicMock()

        create_cominfo_data = ComInfoCreate(
            host_id=self.host_id,
            cpu_utilization=self.cpu_utilization,
            memory_utilization=self.memory_utilization,
            disk_utilization=self.disk_utilization
        )

        created_data = CominfoCRUD(session).create(create_cominfo_data)
        assert created_data.host_id == self.host_id
        assert created_data.cpu_utilization == self.cpu_utilization
        assert created_data.memory_utilization == self.memory_utilization
        assert created_data.disk_utilization == self.disk_utilization

    def test_create_fail_by_db_error(self):
        """데이터 생성 실패(DB 에러 발생)"""
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        create_cominfo_data = ComInfoCreate(
            host_id=self.host_id,
            cpu_utilization=self.cpu_utilization,
            memory_utilization=self.memory_utilization,
            disk_utilization=self.disk_utilization,
            make_datetime=self.make_datetime
        )

        with pytest.raises(crud_error.DatabaseCreateErr):
            CominfoCRUD(session).create(create_cominfo_data)

    def test_get_by_datetime_success_1(self):
        """데이터 날짜로 가져오기 성공(str_dt, end_dt 없는 경우)"""
        data_len = 9
        response_data = [
            {
                "host_id": self.host_id,
                "cpu_utilization": 10.0 * idx,
                "memory_utilization": 11.0 * idx,
                "disk_utilization": 15.0 * idx,
                "make_datetime": datetime.now(),
            } for idx in range(data_len)
        ]

        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(ComInfo),
              mock.call.filter(ComInfo.host_id == self.host_id)],
             [ComInfo(**data) for data in response_data])
        ])

        request_cominfo_get = ComInfoGet(host_id=self.host_id)

        result = CominfoCRUD(session).get_by_datetime(cominfo=request_cominfo_get)

        assert len(result) == data_len
        for idx in range(data_len):
            assert result[idx].host_id == response_data[idx].get("host_id")
            assert result[idx].cpu_utilization == response_data[idx].get("cpu_utilization")
            assert result[idx].memory_utilization == response_data[idx].get("memory_utilization")
            assert result[idx].disk_utilization == response_data[idx].get("disk_utilization")
            assert result[idx].make_datetime == response_data[idx].get("make_datetime")

    def test_get_by_datetime_success_2(self):
        """데이터 날짜로 가져오기 성공(end_dt 없는 경우)"""
        data_len = 9
        response_data = [
            {
                "host_id": self.host_id,
                "cpu_utilization": 10.0 * idx,
                "memory_utilization": 11.0 * idx,
                "disk_utilization": 15.0 * idx,
                "make_datetime": datetime.now(),
            } for idx in range(data_len)
        ]

        start_dt = datetime.now()

        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(ComInfo),
              mock.call.filter(ComInfo.host_id == self.host_id,
                               ComInfo.make_datetime >= start_dt)],
             [ComInfo(**data) for data in response_data])
        ])

        request_cominfo_get = ComInfoGet(host_id=self.host_id)
        result = CominfoCRUD(session).get_by_datetime(cominfo=request_cominfo_get, start_dt=start_dt)

        assert len(result) == data_len
        for idx in range(data_len):
            assert result[idx].host_id == response_data[idx].get("host_id")
            assert result[idx].cpu_utilization == response_data[idx].get("cpu_utilization")
            assert result[idx].memory_utilization == response_data[idx].get("memory_utilization")
            assert result[idx].disk_utilization == response_data[idx].get("disk_utilization")
            assert result[idx].make_datetime == response_data[idx].get("make_datetime")

    def test_get_by_datetime_success_3(self):
        """데이터 날짜로 가져오기 성공(start_dt 없는 경우)"""
        data_len = 9
        response_data = [
            {
                "host_id": self.host_id,
                "cpu_utilization": 10.0 * idx,
                "memory_utilization": 11.0 * idx,
                "disk_utilization": 15.0 * idx,
                "make_datetime": datetime.now(),
            } for idx in range(data_len)
        ]

        end_dt = datetime.now()

        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(ComInfo),
              mock.call.filter(ComInfo.host_id == self.host_id,
                               ComInfo.make_datetime <= end_dt)],
             [ComInfo(**data) for data in response_data])
        ])

        request_cominfo_get = ComInfoGet(host_id=self.host_id)
        result = CominfoCRUD(session).get_by_datetime(cominfo=request_cominfo_get, end_dt=end_dt)

        assert len(result) == data_len
        for idx in range(data_len):
            assert result[idx].host_id == response_data[idx].get("host_id")
            assert result[idx].cpu_utilization == response_data[idx].get("cpu_utilization")
            assert result[idx].memory_utilization == response_data[idx].get("memory_utilization")
            assert result[idx].disk_utilization == response_data[idx].get("disk_utilization")
            assert result[idx].make_datetime == response_data[idx].get("make_datetime")

    def test_get_by_datetime_success_4(self):
        """데이터 날짜로 가져오기 성공(모든 파라미터가 있는 경우)"""
        data_len = 9
        response_data = [
            {
                "host_id": self.host_id,
                "cpu_utilization": 10.0 * idx,
                "memory_utilization": 11.0 * idx,
                "disk_utilization": 15.0 * idx,
                "make_datetime": datetime.now(),
            } for idx in range(data_len)
        ]

        start_dt = datetime.now()
        end_dt = datetime.now()

        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(ComInfo),
              mock.call.filter(ComInfo.host_id == self.host_id,
                               ComInfo.make_datetime >= start_dt,
                               ComInfo.make_datetime <= end_dt)],
             [ComInfo(**data) for data in response_data])
        ])

        request_cominfo_get = ComInfoGet(host_id=self.host_id)
        result = CominfoCRUD(session).get_by_datetime(cominfo=request_cominfo_get, start_dt=start_dt, end_dt=end_dt)

        assert len(result) == data_len
        for idx in range(data_len):
            assert result[idx].host_id == response_data[idx].get("host_id")
            assert result[idx].cpu_utilization == response_data[idx].get("cpu_utilization")
            assert result[idx].memory_utilization == response_data[idx].get("memory_utilization")
            assert result[idx].disk_utilization == response_data[idx].get("disk_utilization")
            assert result[idx].make_datetime == response_data[idx].get("make_datetime")

    def test_get_multiline_success_1(self):
        """데이터 여러개 가져오기(skip, limit없는 경우)"""
        data_len = 9
        response_data = [
            {
                "host_id": self.host_id,
                "cpu_utilization": 10.0 * idx,
                "memory_utilization": 11.0 * idx,
                "disk_utilization": 15.0 * idx,
                "make_datetime": datetime.now(),
            } for idx in range(data_len)
        ]

        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(ComInfo),
              mock.call.filter(ComInfo.host_id == self.host_id),
              mock.call.offset(0),
              mock.call.limit(1000)],
             [ComInfo(**data) for data in response_data])
        ])

        request_cominfo_get = ComInfoGet(host_id=self.host_id)
        result = CominfoCRUD(session).get_multiline(cominfo=request_cominfo_get)

        assert len(result) == data_len
        for idx in range(data_len):
            assert result[idx].host_id == response_data[idx].get("host_id")
            assert result[idx].cpu_utilization == response_data[idx].get("cpu_utilization")
            assert result[idx].memory_utilization == response_data[idx].get("memory_utilization")
            assert result[idx].disk_utilization == response_data[idx].get("disk_utilization")
            assert result[idx].make_datetime == response_data[idx].get("make_datetime")

    def test_get_multiline_success_2(self):
        """데이터 여러개 가져오기(limit없는 경우)"""
        data_len = 9
        response_data = [
            {
                "host_id": self.host_id,
                "cpu_utilization": 10.0 * idx,
                "memory_utilization": 11.0 * idx,
                "disk_utilization": 15.0 * idx,
                "make_datetime": datetime.now(),
            } for idx in range(data_len)
        ]
        skip = 3

        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(ComInfo),
              mock.call.filter(ComInfo.host_id == self.host_id),
              mock.call.offset(skip),
              mock.call.limit(1000)],
             [ComInfo(**data) for data in response_data])
        ])

        request_cominfo_get = ComInfoGet(host_id=self.host_id)
        result = CominfoCRUD(session).get_multiline(cominfo=request_cominfo_get, skip=skip)

        assert len(result) == data_len
        for idx in range(data_len):
            assert result[idx].host_id == response_data[idx].get("host_id")
            assert result[idx].cpu_utilization == response_data[idx].get("cpu_utilization")
            assert result[idx].memory_utilization == response_data[idx].get("memory_utilization")
            assert result[idx].disk_utilization == response_data[idx].get("disk_utilization")
            assert result[idx].make_datetime == response_data[idx].get("make_datetime")

    def test_get_multiline_success_3(self):
        """데이터 여러개 가져오기(skip 없는 경우)"""
        data_len = 9
        response_data = [
            {
                "host_id": self.host_id,
                "cpu_utilization": 10.0 * idx,
                "memory_utilization": 11.0 * idx,
                "disk_utilization": 15.0 * idx,
                "make_datetime": datetime.now(),
            } for idx in range(data_len)
        ]
        limit = 50

        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(ComInfo),
              mock.call.filter(ComInfo.host_id == self.host_id),
              mock.call.offset(0),
              mock.call.limit(limit)],
             [ComInfo(**data) for data in response_data])
        ])

        request_cominfo_get = ComInfoGet(host_id=self.host_id)
        result = CominfoCRUD(session).get_multiline(cominfo=request_cominfo_get, limit=limit)

        assert len(result) == data_len
        for idx in range(data_len):
            assert result[idx].host_id == response_data[idx].get("host_id")
            assert result[idx].cpu_utilization == response_data[idx].get("cpu_utilization")
            assert result[idx].memory_utilization == response_data[idx].get("memory_utilization")
            assert result[idx].disk_utilization == response_data[idx].get("disk_utilization")
            assert result[idx].make_datetime == response_data[idx].get("make_datetime")

    def test_get_multiline_success_4(self):
        """데이터 여러개 가져오기(모든 파라미터가 있는 경우)"""
        data_len = 9
        response_data = [
            {
                "host_id": self.host_id,
                "cpu_utilization": 10.0 * idx,
                "memory_utilization": 11.0 * idx,
                "disk_utilization": 15.0 * idx,
                "make_datetime": datetime.now(),
            } for idx in range(data_len)
        ]
        skip = 5
        limit = 50

        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(ComInfo),
              mock.call.filter(ComInfo.host_id == self.host_id),
              mock.call.offset(skip),
              mock.call.limit(limit)],
             [ComInfo(**data) for data in response_data])
        ])

        request_cominfo_get = ComInfoGet(host_id=self.host_id)
        result = CominfoCRUD(session).get_multiline(cominfo=request_cominfo_get, skip=skip, limit=limit)

        assert len(result) == data_len
        for idx in range(data_len):
            assert result[idx].host_id == response_data[idx].get("host_id")
            assert result[idx].cpu_utilization == response_data[idx].get("cpu_utilization")
            assert result[idx].memory_utilization == response_data[idx].get("memory_utilization")
            assert result[idx].disk_utilization == response_data[idx].get("disk_utilization")
            assert result[idx].make_datetime == response_data[idx].get("make_datetime")

    def test_get_by_datetime_fail_with_db_error(self):
        """데이터 날짜로 가져오기 실패(Db error)"""
        session = AlchemyMagicMock()
        session.query.side_effect = SQLAlchemyError()

        request_cominfo_get = ComInfoGet(host_id=self.host_id)

        with pytest.raises(crud_error.DatabaseGetErr):
            CominfoCRUD(session).get_by_datetime(cominfo=request_cominfo_get)

    def test_get_multiline_fail_with_db_error(self):
        """데이터 여러개 가져오기 실패(Db error)"""
        session = AlchemyMagicMock()
        session.query.side_effect = SQLAlchemyError()

        request_cominfo_get = ComInfoGet(host_id=self.host_id)

        with pytest.raises(crud_error.DatabaseGetErr):
            CominfoCRUD(session).get_multiline(cominfo=request_cominfo_get)


class TestCominfoRtCRUD:
    host_id = 1
    cpu_utilization = 20.5
    memory_utilization = 30.0
    disk_utilization = 40.3
    make_datetime = datetime.now()
    update_datetime = datetime.now()

    def test_create_success(self):
        """데이터 생성 성공"""
        session = AlchemyMagicMock()

        create_cominfort_data = ComInfoRTGet(host_id=self.host_id,
                                             cpu_utilization=self.cpu_utilization,
                                             memory_utilization=self.memory_utilization,
                                             disk_utilization=self.disk_utilization)
        created_data = CominfoRtCRUD(session).create(cominfo=create_cominfort_data)

        assert created_data.host_id == self.host_id
        assert created_data.cpu_utilization == self.cpu_utilization
        assert created_data.memory_utilization == self.memory_utilization
        assert created_data.disk_utilization == self.disk_utilization

    def test_create_fail_by_db_error(self):
        """데이터 생성 실패(DB 에러 발생)"""
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        create_cominfort_data = ComInfoRTGet(host_id=self.host_id)
        with pytest.raises(crud_error.DatabaseCreateErr):
            CominfoRtCRUD(session).create(cominfo=create_cominfort_data)

    def test_get_success(self):
        """데이터 가져오기 성공"""
        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(ComInfoRT),
              mock.call.filter(ComInfoRT.host_id == self.host_id)],
             [ComInfoRTGet(
                 host_id=self.host_id,
                 cpu_utilization=self.cpu_utilization,
                 memory_utilization=self.memory_utilization,
                 disk_utilization=self.disk_utilization
             )])
        ])

        request_cominfo_data = ComInfoRTGet(host_id=self.host_id)
        result = CominfoRtCRUD(session).get(cominfo=request_cominfo_data)

        assert result.host_id == self.host_id
        assert result.cpu_utilization == self.cpu_utilization
        assert result.memory_utilization == self.memory_utilization
        assert result.disk_utilization == self.disk_utilization

    def test_get_fail_with_db_error(self):
        """데이터 가져오기 실패(DB error)"""
        session = AlchemyMagicMock()
        session.query.side_effect = SQLAlchemyError()

        request_cominfo_data = ComInfoRTGet(host_id=self.host_id)
        with pytest.raises(crud_error.DatabaseGetErr):
            result = CominfoRtCRUD(session).get(request_cominfo_data)

    def test_update_success(self):
        """데이터 수정 성공"""
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 1

        update_data = ComInfoRTGet(host_id=self.host_id)
        CominfoRtCRUD(session).update(update_data=update_data)

    def test_update_fail_by_db_error(self):
        """데이터 수정 실패 (DB 에러 발생)"""
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        update_data = ComInfoRTGet(host_id=self.host_id)
        with pytest.raises(crud_error.DatabaseUpdateErr):
            CominfoRtCRUD(session).update(update_data=update_data)
