from unittest import mock

import pytest
from mock_alchemy.mocking import AlchemyMagicMock, UnifiedAlchemyMagicMock
from sqlalchemy.exc import SQLAlchemyError

from app.api.commanage import model as model
from app.api.commanage.schema import ComManageByUser, ComManageByHost
from app.api.commanage.crud import CommanageCRUD

from app.api.exception import crud_error


class TestCommanageCRUD:
    user_id = "test_user"
    host_id = 1
    host_name = "host1"
    host_ip = "127.0.0.1"
    memory = "16G"
    disk = "32G"
    deleted = False

    def test_create_success(self):
        """데이터 생성 성공"""
        session = AlchemyMagicMock()
        create_commanage_data = ComManageByUser(user_id=self.user_id,
                                                host_id=self.host_id,
                                                host_name=self.host_name,
                                                host_ip=self.host_ip,
                                                memory=self.memory,
                                                disk=self.disk,
                                                deleted=self.deleted)
        created_user = CommanageCRUD(session).create(create_commanage_data)

        assert created_user.user_id == self.user_id
        assert created_user.host_id == self.host_id
        assert created_user.host_name == self.host_name
        assert created_user.host_ip == self.host_ip
        assert created_user.memory == self.memory
        assert created_user.disk == self.disk
        assert created_user.deleted == self.deleted

    def test_create_fail_by_db_error(self):
        """데이터 생성 실패(DB 에러 발생)"""
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        create_commanage_data = ComManageByUser(user_id=self.user_id)
        with pytest.raises(crud_error.DatabaseCreateErr):
            CommanageCRUD(session).create(create_commanage_data)

    def test_update_success(self):
        """데이터 수정 성공"""
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 1

        update_data = ComManageByHost(host_id=self.host_id)
        CommanageCRUD(session).update(update_data=update_data)

    def test_update_fail_by_db_error(self):
        """데이터 수정 실패 (DB 에러 발생)"""
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        update_data = ComManageByHost(host_id=self.host_id)
        with pytest.raises(crud_error.DatabaseUpdateErr):
            CommanageCRUD(session).update(update_data=update_data)

    def test_delete_success(self):
        """데이터 삭제 성공"""
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 1

        delete_data = ComManageByHost(host_id=self.host_id)
        CommanageCRUD(session).delete(delete_data=delete_data)

    def test_delete_fail_by_db_error(self):
        """삭제된 데이터가 없는 경우"""
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        delete_data = ComManageByHost(host_id=self.host_id)
        with pytest.raises(crud_error.DatabaseDeleteErr):
            CommanageCRUD(session).delete(delete_data=delete_data)

    def test_delete_all_succes(self):
        """사용자에 해당하는 Commanage 전체 삭제 성공"""
        session = AlchemyMagicMock()
        session.query.return_value.filter.return_value.update.return_value = 1

        delete_data = ComManageByHost(host_id=self.host_id)
        CommanageCRUD(session).delete(delete_data=delete_data)

    def test_delete_all_fail_by_db_error(self):
        """사용자에 해당하는 Commanage 전체 삭제 실패(DB 에러 발생)"""
        session = AlchemyMagicMock()
        session.commit.side_effect = SQLAlchemyError()

        delete_data = ComManageByUser(user_id=self.user_id)
        with pytest.raises(crud_error.DatabaseDeleteErr):
            CommanageCRUD(session).delete_all(commanage=delete_data)

    def test_get_success(self):
        """데이터 가져오기 성공"""
        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(model.ComManage),
              mock.call.filter(model.ComManage.host_id == self.host_id)],
             [model.ComManage(
                 user_id=self.user_id,
                 host_id=self.host_id,
                 host_name=self.host_name,
                 host_ip=self.host_ip,
                 memory=self.memory,
                 disk=self.disk,
                 deleted=self.deleted)]
             )
        ])

        request_commange_data = ComManageByHost(host_id=self.host_id)
        result = CommanageCRUD(session).get(commanage=request_commange_data)

        assert result.user_id == self.user_id
        assert result.host_id == self.host_id
        assert result.host_name == self.host_name
        assert result.host_ip == self.host_ip
        assert result.memory == self.memory
        assert result.disk == self.disk
        assert result.deleted == self.deleted

    def test_get_fail_by_db_error(self):
        """데이터 가져오기 실패(DB error)"""
        session = AlchemyMagicMock()
        session.query.side_effect = SQLAlchemyError()

        request_commange_data = ComManageByHost(host_id=self.host_id)

        with pytest.raises(crud_error.DatabaseGetErr):
            CommanageCRUD(session).get(commanage=request_commange_data)

    def test_get_all_success(self):
        """데이터 전체 가져오기 성공"""
        data_get_len = 9
        test_data = [{
            "user_id": self.user_id,
            "host_id": idx,
            "host_name": f"host{idx}",
            "host_ip": f"127.0.0.1",
            "memory": f"12G",
            "disk": f"256G",
            "deleted": False
        } for idx in range(data_get_len)
        ]

        session = UnifiedAlchemyMagicMock(data=[
            ([mock.call.query(model.ComManage),
              mock.call.filter(model.ComManage.user_id == self.user_id)],
             [model.ComManage(**data) for data in test_data])
        ])

        request_commange_data = ComManageByUser(user_id=self.user_id)
        result = CommanageCRUD(session).get_all(commanage=request_commange_data)

        assert len(result) == data_get_len
        for idx in range(data_get_len):
            assert result[idx].user_id == test_data[idx].get("user_id")
            assert result[idx].host_id == test_data[idx].get("host_id")
            assert result[idx].host_name == test_data[idx].get("host_name")
            assert result[idx].host_ip == test_data[idx].get("host_ip")
            assert result[idx].memory == test_data[idx].get("memory")
            assert result[idx].disk == test_data[idx].get("disk")
            assert result[idx].deleted == test_data[idx].get("deleted")

    def test_get_all_fail_by_db_error(self):
        """데이터 전체 가져오기 실패(DB error)"""
        session = AlchemyMagicMock()
        session.query.side_effect = SQLAlchemyError()

        request_commange_data = ComManageByUser(user_id=self.user_id)

        with pytest.raises(crud_error.DatabaseGetErr):
            CommanageCRUD(session).get_all(commanage=request_commange_data)
