from typing import Any
import aiohttp
from aiohttp.client_exceptions import ClientError


class HttpRequestError(Exception):
    pass


class HttpRequest:
    """
    Http Request 전송 기능 구현 클래스
    """

    def __init__(self, api_url: str, data: Any, header: Any):
        """
        생성자
        :param api_url: 전송할 API url
        :param data: 전송할 데이터
        :param header: 전송할 헤더
        """
        self.request_param = {"url": api_url, "data": data, "headers": header}

    async def post(self):
        """
        post 메서드로 전송
        :return:
        """
        try:
            async with aiohttp.ClientSession() as session:
                result = await session.post(**self.request_param)
                return result.status, await result.json()
        except ClientError as err:
            raise HttpRequestError(f"post error : {err}")

    async def put(self):
        """
        put 메서드로 전송
        :return:
        """
        try:
            async with aiohttp.ClientSession() as session:
                result = await session.put(**self.request_param)
                return result.status, await result.json()
        except ClientError as err:
            raise HttpRequestError(f"put error : {err}")
