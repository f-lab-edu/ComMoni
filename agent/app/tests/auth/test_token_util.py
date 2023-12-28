import pytest

import app.auth.token_util
from app.auth.token_util import TokenUtil, TokenUtilError


class TestTokenUtil:
    file_path = "file_path"

    def test_read_file_1(self, mocker):
        mocker.patch("builtins.open", return_value=mocker.MagicMock())

        TokenUtil(file_path=self.file_path).read_file()

    def test_read_file_2(self, mocker):
        mocker.patch("builtins.open", return_value=mocker.MagicMock()) \
            .side_effect = OSError()

        with pytest.raises(TokenUtilError):
            TokenUtil(file_path=self.file_path).read_file()

    def test_write_file_1(self, mocker):
        mocker.patch("builtins.open", return_value=mocker.MagicMock())

        token_util = TokenUtil(file_path=self.file_path)
        token_util.token = "token"
        token_util.write_file()

    def test_write_file_2(self, mocker):
        mocker.patch("builtins.open", return_value=mocker.MagicMock())

        token_util = TokenUtil(file_path=self.file_path)

        with pytest.raises(TokenUtilError):
            token_util.write_file()

    def test_write_file_3(self, mocker):
        mocker.patch("builtins.open", return_value=mocker.MagicMock()) \
            .side_effect = OSError()

        with pytest.raises(TokenUtilError):
            TokenUtil(file_path=self.file_path).write_file()

    def test_parse_payload_1(self, mocker):
        """parse payload test"""
        mocker.patch("base64.b64decode", return_value="{'a':15}".encode('utf-8'))

        token_util = TokenUtil(file_path=self.file_path)
        token_util.token = "header.payload.fingerprint"

        token_util.parse_payload()

    def test_parse_payload_2(self, mocker):
        """parse payload test"""
        mocker.patch("base64.b64decode", return_value="{'a':15}".encode('utf-8'))

        token_util = TokenUtil(file_path=self.file_path)
        token_util.token = ""

        with pytest.raises(TokenUtilError):
            token_util.parse_payload()

    def test_get_host_id_1(self, mocker):
        """get_host_id test"""
        token_util = TokenUtil(file_path=self.file_path)
        token_util.payload = {'host_id': 15}

        assert token_util.get_host_id() == 15

    def test_get_host_id_2(self, mocker):
        """get_host_id test"""
        token_util = TokenUtil(file_path=self.file_path)
        token_util.payload = {}

        with pytest.raises(TokenUtilError):
            token_util.get_host_id()

    def test_get_user_id_1(self, mocker):
        """get_user_id test"""
        token_util = TokenUtil(file_path=self.file_path)
        token_util.payload = {'user_id': 15}

        assert token_util.get_user_id() == 15

    def test_get_user_id_2(self, mocker):
        """get_user_id test"""
        token_util = TokenUtil(file_path=self.file_path)
        token_util.payload = {}

        with pytest.raises(TokenUtilError):
            token_util.get_user_id()
