import configparser

from app.configs.log import logger


class Settings:
    # request interval
    REALTIME_INTERVAL: int = 10  # secondss
    NORMAL_INTERVAL: int = 30  # second

    # API
    API_SERVER_URL: str = "http://localhost:8000"
    API_USER_ID: str = "tester"
    API_USER_PW: str = "1234567890"
    HOST_NAME: str = "tester_host_1"

    API_LOGIN_PATH: str = "/api/v1/auth/login"
    API_REGIST_COMMANAGE: str = "/api/v1/auth/register-commanage"
    API_COMINFO_PATH: str = "/api/v1/cominfo"
    API_COMINFO_RT_PATH: str = "/api/v1/cominfo/realtime"

    # token
    TOKEN_FILE_PATH: str = "./token.txt"


settings = Settings()
