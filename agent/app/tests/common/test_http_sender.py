import pytest

from aiohttp.client_exceptions import ClientError
from app.common.http_sender import HttpSender, HttpError


class TestHttpSender:
    api_url = "api_url"
    data = "data"
    token = "token"
    header = {"header": "header_data"}

    def test_get_api_header(self):
        """http api header 생성 테스트"""
        api_header = {"Content-Type": "application/json",
                      "accept": "application/json",
                      "authorization": f"Bearer {self.token}"}
        assert HttpSender.get_api_header(self.token) == api_header

    def test_get_login_header(self):
        """http login header 생성 테스트"""
        login_header = {"Content-Type": "application/x-www-form-urlencoded",
                        "accept": "application/json"}
        assert HttpSender.get_login_header() == login_header

    @pytest.mark.asyncio
    def test_post_1(self, mocker):
        """httpsender post 테스트"""
        session = mocker.Mock()
        mocker.patch("aiohttp.ClientSession", return_value=session)

        HttpSender(api_url=self.api_url, data=self.data, header=self.header).post()

    # @pytest.mark.asyncio
    # def test_post_2(self, mocker):
    #     session = mocker.AsyncMock()
    #     session.__aenter__.post.side_effect = ClientError()
    #     mocker.patch("aiohttp.ClientSession", return_value=session)
    #
    #     with pytest.raises(HttpError):
    #         HttpSender(api_url=self.api_url, data=self.data, header=self.header).post()

    @pytest.mark.asyncio
    def test_put_1(self, mocker):
        """httpsender put 테스트"""
        session = mocker.Mock()
        mocker.patch("aiohttp.ClientSession", return_value=session)

        HttpSender(api_url=self.api_url, data=self.data, header=self.header).put()
