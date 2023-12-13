class TokenHandler:
    def __init__(self):
        self.__access_token = ""
        self.__refresh_token = ""

    def set_access_token(self, token: str):
        self.__access_token = token

    def set_refresh_token(self, token: str):
        self.__refresh_token = token

    def get_access_token(self):
        return self.__access_token

    def get_refresh_token(self):
        return self.__refresh_token


token_handler = TokenHandler()
