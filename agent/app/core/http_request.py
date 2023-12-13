from typing import Any
import aiohttp


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

    async def post(self) -> Any:
        """
        post 메서드로 전송
        :return:
        """
        async with aiohttp.ClientSession() as session:
            response = await session.post(**self.request_param)
            print(await response.json())

    async def put(self) -> Any:
        """
        put 메서드로 전송
        :return:
        """
        async with aiohttp.ClientSession() as session:
            response = await session.put(**self.request_param)
            print(await response.json())
