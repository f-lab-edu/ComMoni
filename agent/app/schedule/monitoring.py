import asyncio

from aiohttp.client_exceptions import ClientConnectorError

from app.common.http_sender import HttpSender, HttpError
from app.req_data.monitoring import MonitoringData

from app.auth.login_manager import login_manager
from app.configs.config import settings
from app.configs.log import logger


async def send_rt_monitoring():
    """
    실시간 모니터링 데이터 생성 및 서버 전송
    """
    try:
        token_util = login_manager.get_token_util()
        host_id = token_util.get_host_id()
        api_url = f"{settings.API_SERVER_URL}{settings.API_COMINFO_RT_PATH}"
        header = HttpSender.get_api_header(token_util.token)
        data = MonitoringData(host_id=host_id).make()
        result = await HttpSender(api_url=api_url, data=data, header=header).put()
        logger.info(f"[send_rt_monitoring] result : {result}")

    except HttpError as err:
        logger.error(f"[send_rt_monitoring] put err : {err}")
    except ClientConnectorError as err:
        logger.error(f"[send_rt_monitoring] error : {err}")
    except asyncio.CancelledError:
        pass


async def send_monitoring():
    """
    모니터링 데이터 생성 및 서버 전송
    """
    try:
        token_util = login_manager.get_token_util()
        host_id = token_util.get_host_id()
        api_url = f"{settings.API_SERVER_URL}{settings.API_COMINFO_PATH}"
        header = HttpSender.get_api_header(token_util.token)
        data = MonitoringData(host_id=host_id).make()
        result = await HttpSender(api_url=api_url, data=data, header=header).post()

        logger.info(f"[send_monitoring] result : {result}")

    except HttpError as err:
        logger.error(f"[send_monitoring] put err : {err}")
    except ClientConnectorError as err:
        logger.error(f"[send_monitoring] error : {err}")
    except asyncio.CancelledError:
        pass
