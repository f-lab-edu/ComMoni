import asyncio
from http import HTTPStatus

from app.request.http_request import HttpRequest, HttpRequestError
from app.request_data import login, commanage

from app.common.ini_util import IniUtil, IniUtilError
from app.configs.config import settings
from app.configs.log import logger


class TokenManager:
    def __init__(self):
        self.access_token = ""
        self.refresh_token = ""
        self.ini_util = IniUtil(settings.HOST_INFO_FILE)
        self.host_id_key = "host_id"
        self.host_id = 0

        self.load_ini_file()

    def load_ini_file(self):
        try:
            self.ini_util.load()
        except IniUtilError as err:
            logger.error(f"[Token Manager] {err}")
            logger.error(f"[Token Manager] agent stop...")
            exit(-1)

        host_id = self.ini_util.read(self.host_id_key)
        self.host_id = int(host_id)
        self.init_token()

    def init_token(self):
        if self.host_id == 0:
            # host_id가 0 인 경우는 아직 commanage에 등록을 안한 상태
            # userid/userpw로 로그인한 후, 임시 토큰을 얻어서 등록
            self.get_token()
            self.register_host()

        self.get_token()

    def get_token(self):
        header = {"Content-Type": "application/x-www-form-urlencoded",
                  "accept": "application/json"}
        api_url = f"{settings.API_SERVER_URL}{settings.API_LOGIN_PATH}"
        data = login.LoginData(
            username=settings.API_USER_ID,
            password=settings.API_USER_PW,
            host_id=self.host_id
        ).make()

        try:
            status, result = asyncio.run(
                HttpRequest(api_url=api_url, data=data, header=header).post()
            )
        except HttpRequestError as err:
            logger.error(f"[Token Manager] get_token fail : {err}")
            exit(-1)

        if status != HTTPStatus.OK:
            logger.error(f"[Token Manager] {api_url} return status code {status}")
            exit(-1)

        self.access_token = result['access_token']
        self.refresh_token = result['refresh_token']

    def register_host(self):
        header = {"Content-Type": "application/json",
                  "accept": "application/json",
                  "authorization": f"Bearer {self.access_token}"
                  }
        api_url = f"{settings.API_SERVER_URL}{settings.API_COMMANAGE_PATH}"
        data = commanage.CreateData(
            user_id=settings.API_USER_ID,
            host_name="test_host"
        ).make()

        try:
            status, result = asyncio.run(
                HttpRequest(api_url=api_url, data=data, header=header).post()
            )
        except HttpRequestError as err:
            logger.error(f"[Token Manager] register host fail : {err}")
            exit(-1)

        if status != HTTPStatus.CREATED:
            logger.error(f"[Token Manager] {api_url} return status code {status}")
            exit(-1)

        host_id = result['host_id']

        try:
            self.ini_util.add(self.host_id_key, str(host_id))
            self.ini_util.write()
        except IniUtilError as err:
            logger.error(f"[Token Manager] ini util error : {err}")
            exit(-1)

        self.host_id = host_id


token_manager = TokenManager()
