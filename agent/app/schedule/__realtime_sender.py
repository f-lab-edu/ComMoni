import asyncio

from aiohttp.client_exceptions import ClientConnectorError

from app.request.http_request import HttpRequest
from app.request_data.monitoring import MonitoringData

from app.configs.config import settings
from app.configs.log import logger


async def send_reailtime_data():
    """
    실시간 데이터 생성 및 서버 전송하는 기능. 스케줄러에 등록해서 사용
    """
    try:
        host_id = 5
        api_url = f"{settings.API_SERVER_URL}/cominfo/realtime"
        header = {"Content-Type": "application/json"}
        data = MonitoringData(host_id=host_id).make()
        await HttpRequest(api_url=api_url, data=data, header=header).put()
    except ClientConnectorError as err:
        logger.error(f"ClientConnectorError : {err}")
    except asyncio.CancelledError:
        logger.error(f"send_reailtime_data cancelled")
