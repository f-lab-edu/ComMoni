from app.auth.token_util import TokenUtil, TokenUtilError
from app.common.http_sender import HttpSender, HttpError
from app.req_data.login import LoginData
from app.req_data.commanage import CreateCommanageData

from app.configs.config import settings
from app.configs.log import logger


class LoginManagerError(Exception):
    pass


class LoginManager:
    def __init__(self):
        self.access_token = ""
        self.token_util = TokenUtil(file_path=settings.TOKEN_FILE_PATH)

    def load_token(self) -> bool:
        try:
            self.token_util.read_file()
            self.token_util.parse_payload()
            return True
        except TokenUtilError as err:
            logger.info(f"[LoginManager] {err}")
            return False

    def get_token_util(self):
        return self.token_util

    async def login(self):
        login_url = f"{settings.API_SERVER_URL}{settings.API_LOGIN_PATH}"
        login_data = LoginData(
            username=settings.API_USER_ID,
            password=settings.API_USER_PW
        ).make()
        login_header = HttpSender.get_login_header()

        try:
            status, result = await HttpSender(api_url=login_url, data=login_data, header=login_header).post()
        except HttpError as err:
            logger.error(f"[LoginManager] login err : {err}")
            raise LoginManagerError()

        if status != 200:
            logger.error(f"[LoginManager] login fail. status : {status}, result : {result}")
            raise LoginManagerError()

        self.access_token = result.get("access_token")
        logger.info(f"[LoginManager] login success")

    async def regist(self):
        regist_url = f"{settings.API_SERVER_URL}{settings.API_REGIST_COMMANAGE}"
        regist_data = CreateCommanageData(
            user_id=settings.API_USER_ID,
            host_name=settings.HOST_NAME
        ).make()
        api_header = HttpSender.get_api_header(self.access_token)

        try:
            status, result = await HttpSender(api_url=regist_url, data=regist_data, header=api_header).post()
        except HttpError as err:
            logger.error(f"[LoginManager] regist err : {err}")
            raise LoginManagerError()

        if status != 200:
            logger.error(f"[LoginManager] regist fail. status : {status}, result : {result}")
            raise LoginManagerError()

        agent_token = result.get("value")
        self.token_util.set_token(agent_token)
        logger.info(f"[LoginManager] regist success")

    async def save_agent_token(self):
        try:
            self.token_util.write_file()
        except TokenUtilError as err:
            logger.error(f"[LoginManager] token save fail. err: {err}")
            raise LoginManagerError()


async def login_api_server():
    if not login_manager.load_token():
        logger.info("[login_api_server] agent login api server")

        try:
            logger.info("[login_api_server] login server")
            await login_manager.login()
            logger.info("[login_api_server] regist commanage")
            await login_manager.regist()
            logger.info("[login_api_server] save token")
            await login_manager.save_agent_token()
        except LoginManagerError:
            exit(-1)


login_manager = LoginManager()
